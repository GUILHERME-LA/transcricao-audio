import whisper
import torch
import subprocess
import os
import threading
import time
import shutil
import logging
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict
from datetime import timedelta
import sys
import os

def get_ffmpeg_path():
    # Se estiver empacotado (PyInstaller)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        
        caminho1 = os.path.join(base_path, 'ffmpeg.exe')
        if os.path.exists(caminho1):
            return caminho1

        caminho2 = os.path.join(os.path.dirname(sys.executable), 'ffmpeg.exe')
        if os.path.exists(caminho2):
            return caminho2

    # Se estiver rodando como script
    caminho3 = os.path.join(os.getcwd(), 'ffmpeg.exe')
    if os.path.exists(caminho3):
        return caminho3

    return 'ffmpeg'

# ===== CONFIGURAÇÃO DE LOGGING =====
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(__file__)

log_path = os.path.join(base_path, "transcritor.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===== CONFIGURAÇÕES =====
@dataclass
class Config:
    CHUNK_TIME: int = 300
    MODEL: str = "base"
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
    TEMP_DIR: str = "chunks"
    SUPPORTED_FORMATS: tuple = ("*.mp3", "*.wav", "*.m4a", "*.mp4", "*.mkv", "*.flac", "*.ogg")

config = Config()

# ===== CLASSE PRINCIPAL =====
class TranscriptorApp:
    def __init__(self, root):
        self.root = root
        self.audio_path: str = ""
        self.cancelar: bool = False
        self.model = None
        self.thread_ativa = False
        
        self.setup_ui()
        self.check_dependencies()
    
    def setup_ui(self):
        """Configura a interface do usuário com design moderno"""
        # Aparência
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root.title("🎙️ Transcritor IA - Profissional")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        # Cores customizadas
        self.bg_color = "#1a1a1a"
        self.fg_color = "#ffffff"
        self.accent_color = "#0084ff"
        
        # Frame Principal com padding
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ===== HEADER =====
        header = ctk.CTkFrame(main_frame)
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header,
            text="🎙️ Transcritor de Áudio",
            font=("Helvetica", 28, "bold")
        )
        title.pack(side="left")
        
        device_info = ctk.CTkLabel(
            header,
            text=f"GPU: {config.DEVICE.upper()}",
            font=("Helvetica", 12),
            text_color="#888888"
        )
        device_info.pack(side="right")
        
        # ===== SEÇÃO DE ARQUIVO =====
        file_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a")
        file_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            file_frame,
            text="📁 Selecione o Arquivo",
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        btn_frame = ctk.CTkFrame(file_frame)
        btn_frame.pack(fill="x", padx=15, pady=10)
        
        self.btn_audio = ctk.CTkButton(
            btn_frame,
            text="Escolher Áudio",
            command=self.escolher_audio,
            fg_color=self.accent_color,
            hover_color="#0066cc",
            font=("Helvetica", 12, "bold"),
            height=40
        )
        self.btn_audio.pack(side="left", padx=(0, 10))
        
        self.label_arquivo = ctk.CTkLabel(
            btn_frame,
            text="Nenhum arquivo selecionado",
            font=("Helvetica", 11),
            text_color="#888888"
        )
        self.label_arquivo.pack(side="left", fill="x", expand=True)
        
        # ===== SEÇÃO DE PROGRESSO =====
        progress_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a")
        progress_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            progress_frame,
            text="⚙️ Processamento",
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 10))
        
        prog_info = ctk.CTkFrame(progress_frame)
        prog_info.pack(fill="x", padx=15, pady=(0, 10))
        
        self.status = ctk.CTkLabel(
            prog_info,
            text="Aguardando...",
            font=("Helvetica", 11),
            text_color="#888888"
        )
        self.status.pack(anchor="w")
        
        self.progress = ctk.CTkProgressBar(progress_frame, height=8)
        self.progress.pack(fill="x", padx=15, pady=(0, 10))
        self.progress.set(0)
        
        info_row = ctk.CTkFrame(progress_frame)
        info_row.pack(fill="x", padx=15, pady=(0, 15))
        
        self.tempo_label = ctk.CTkLabel(
            info_row,
            text="⏱️ Tempo estimado: -",
            font=("Helvetica", 10),
            text_color="#888888"
        )
        self.tempo_label.pack(side="left")
        
        self.chunk_label = ctk.CTkLabel(
            info_row,
            text="Chunk: -",
            font=("Helvetica", 10),
            text_color="#888888"
        )
        self.chunk_label.pack(side="right")
        
        # ===== SEÇÃO DE SAÍDA =====
        output_frame = ctk.CTkFrame(main_frame, fg_color="#2a2a2a")
        output_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(
            output_frame,
            text="📝 Transcrição em Tempo Real",
            font=("Helvetica", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 10))
        
        self.textbox = ctk.CTkTextbox(
            output_frame,
            font=("Courier", 10),
            fg_color="#1a1a1a",
            text_color="#e0e0e0"
        )
        self.textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # ===== SEÇÃO DE BOTÕES =====
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        self.btn_iniciar = ctk.CTkButton(
            btn_frame,
            text="▶️  Iniciar Transcrição",
            command=self.iniciar,
            fg_color="#00b32a",
            hover_color="#009a23",
            font=("Helvetica", 13, "bold"),
            height=45
        )
        self.btn_iniciar.pack(side="left", padx=5, expand=True, fill="x")
        
        self.btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="⛔ Cancelar",
            command=self.cancelar_exec,
            fg_color="#ff3333",
            hover_color="#cc0000",
            font=("Helvetica", 13, "bold"),
            height=45,
            state="disabled"
        )
        self.btn_cancelar.pack(side="left", padx=5, expand=True, fill="x")
        
        btn_copiar = ctk.CTkButton(
            btn_frame,
            text="📋 Copiar Texto",
            command=self.copiar_texto,
            fg_color="#666666",
            hover_color="#888888",
            font=("Helvetica", 13, "bold"),
            height=45
        )
        btn_copiar.pack(side="left", padx=5, expand=True, fill="x")
    
    def check_dependencies(self):
        """Verifica dependências necessárias"""
        try:
            subprocess.run(
                [get_ffmpeg_path(), "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            messagebox.showerror(
                "Erro",
                "FFmpeg não encontrado!\n\nPor favor, instale FFmpeg:\n"
                "https://ffmpeg.org/download.html"
            )
            logger.error("FFmpeg não está instalado")
    
    def escolher_audio(self):
        """Abre diálogo para selecionar arquivo de áudio"""
        if self.thread_ativa:
            messagebox.showwarning("Aviso", "Uma transcrição já está em andamento!")
            return
        
        tipos = [
            ("Arquivos de Mídia", " ".join(config.SUPPORTED_FORMATS)),
            ("Vídeos MP4", "*.mp4"),
            ("Áudio MP3", "*.mp3"),
            ("Todos", "*.*")
        ]
        
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo de áudio/vídeo",
            filetypes=tipos
        )
        
        if caminho:
            self.audio_path = caminho
            nome = Path(caminho).name
            self.label_arquivo.configure(text=f"✅ {nome}")
            logger.info(f"Arquivo selecionado: {caminho}")
    
    def converter_audio(self) -> bool:
        """Converte áudio para formato compatível com Whisper"""
        try:
            self.status.configure(text="🔄 Convertendo áudio...")
            self.root.update()
            
            novo_arquivo = "audio_convertido.wav"
            
            subprocess.run(
                [
                    get_ffmpeg_path(), "-y", "-i", self.audio_path,
                    "-ar", "16000", "-ac", "1", novo_arquivo
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=300
            )
            
            self.audio_path = novo_arquivo
            logger.info("Áudio convertido com sucesso")
            return True
        
        except subprocess.TimeoutExpired:
            logger.error("Timeout ao converter áudio")
            self.status.configure(text="❌ Timeout na conversão")
            return False
        except Exception as e:
            logger.error(f"Erro ao converter áudio: {e}")
            self.status.configure(text=f"❌ Erro: {e}")
            return False
    
    def dividir_audio(self) -> bool:
        """Divide o áudio em chunks para processamento"""
        try:
            self.status.configure(text="🔪 Dividindo áudio...")
            self.root.update()
            
            if os.path.exists(config.TEMP_DIR):
                shutil.rmtree(config.TEMP_DIR)
            os.mkdir(config.TEMP_DIR)
            
            subprocess.run(
                [
                    get_ffmpeg_path(), "-i", self.audio_path,
                    "-f", "segment", "-segment_time", str(config.CHUNK_TIME),
                    "-acodec", "pcm_s16le", f"{config.TEMP_DIR}/parte_%03d.wav"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=300
            )
            
            logger.info("Áudio dividido com sucesso")
            return True
        
        except Exception as e:
            logger.error(f"Erro ao dividir áudio: {e}")
            self.status.configure(text=f"❌ Erro: {e}")
            return False
    
    def formatar_tempo(self, segundos: float) -> str:
        """Formata tempo em HH:MM:SS,mmm"""
        h = int(segundos // 3600)
        m = int((segundos % 3600) // 60)
        s = int(segundos % 60)
        ms = int((segundos % 1) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    
    def salvar_srt(self, segmentos: List[Dict], caminho: str):
        """Salva transcrição em formato SRT"""
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                for i, seg in enumerate(segmentos, 1):
                    inicio = self.formatar_tempo(seg.get("start", 0))
                    fim = self.formatar_tempo(seg.get("end", 0))
                    texto = seg.get("text", "").strip()
                    
                    if texto:
                        f.write(f"{i}\n{inicio} --> {fim}\n{texto}\n\n")
            
            logger.info(f"SRT salvo: {caminho}")
        except Exception as e:
            logger.error(f"Erro ao salvar SRT: {e}")
    
    def transcrever(self):
        """Função principal de transcrição"""
        self.cancelar = False
        self.thread_ativa = True
        
        try:
            # Validações
            if not self.audio_path:
                messagebox.showerror("Erro", "Por favor, selecione um arquivo!")
                self.thread_ativa = False
                return
            
            # Reset UI
            self.progress.set(0)
            self.textbox.delete("1.0", "end")
            self.btn_iniciar.configure(state="disabled")
            self.btn_cancelar.configure(state="normal")
            self.btn_audio.configure(state="disabled")
            
            # Conversão e divisão
            if not self.converter_audio():
                self.thread_ativa = False
                return
            
            if not self.dividir_audio():
                self.thread_ativa = False
                return
            
            # Processamento
            arquivos = sorted(os.listdir(config.TEMP_DIR))
            total = len(arquivos)
            
            self.status.configure(text=f"📥 Carregando modelo {config.MODEL}...")
            self.root.update()
            
            model = whisper.load_model(config.MODEL).to(config.DEVICE)
            
            inicio = time.time()
            todos_segmentos = []
            
            # Nomes de saída
            nome_base = Path(self.audio_path).stem
            pasta_audio = Path(self.audio_path).parent
            
            output_txt = pasta_audio / f"{nome_base}.txt"
            output_srt = pasta_audio / f"{nome_base}.srt"
            
            with open(output_txt, "w", encoding="utf-8") as f:
                for i, arq in enumerate(arquivos):
                    if self.cancelar:
                        self.status.configure(text="⛔ Cancelado pelo usuário")
                        logger.info("Transcrição cancelada")
                        break
                    
                    caminho = os.path.join(config.TEMP_DIR, arq)
                    
                    self.status.configure(text=f"🧠 Processando: {arq} ({i+1}/{total})")
                    self.chunk_label.configure(text=f"Chunk: {i+1}/{total}")
                    self.root.update()
                    
                    result = model.transcribe(caminho)
                    
                    texto = result.get("text", "").strip()
                    segmentos = result.get("segments", [])
                    
                    todos_segmentos.extend(segmentos)
                    
                    if texto:
                        f.write(texto + "\n")
                        self.textbox.insert("end", texto + "\n")
                        self.textbox.see("end")
                    
                    self.progress.set((i + 1) / total)
                    
                    # Tempo estimado
                    tempo_passado = time.time() - inicio
                    media = tempo_passado / (i + 1)
                    restante = media * (total - (i + 1))
                    
                    self.tempo_label.configure(
                        text=f"⏱️ Tempo estimado: {str(timedelta(seconds=int(restante)))}"
                    )
            
            if not self.cancelar and todos_segmentos:
                self.salvar_srt(todos_segmentos, str(output_srt))
                
                self.status.configure(
                    text=f"✅ Sucesso!\n\n📄 {output_txt.name}\n🎬 {output_srt.name}"
                )
                logger.info(f"Transcrição concluída: {output_txt}")
                messagebox.showinfo("Sucesso", f"Arquivos salvos:\n{output_txt}\n{output_srt}")
            
        except Exception as e:
            logger.error(f"Erro na transcrição: {e}")
            self.status.configure(text=f"❌ Erro: {str(e)[:50]}")
            messagebox.showerror("Erro", f"Erro durante transcrição:\n{e}")
        
        finally:
            self.thread_ativa = False
            self.btn_iniciar.configure(state="normal")
            self.btn_cancelar.configure(state="disabled")
            self.btn_audio.configure(state="normal")
            
            # Limpeza
            if os.path.exists(config.TEMP_DIR):
                shutil.rmtree(config.TEMP_DIR)
            
            if os.path.exists("audio_convertido.wav"):
                os.remove("audio_convertido.wav")
    
    def iniciar(self):
        """Inicia transcrição em thread separada"""
        thread = threading.Thread(target=self.transcrever, daemon=True)
        thread.start()
    
    def cancelar_exec(self):
        """Cancela a transcrição"""
        self.cancelar = True
        self.status.configure(text="⏹️ Cancelando...")
    
    def copiar_texto(self):
        """Copia o texto transcrito para clipboard"""
        try:
            texto = self.textbox.get("1.0", "end")
            if texto.strip():
                self.root.clipboard_clear()
                self.root.clipboard_append(texto)
                messagebox.showinfo("Sucesso", "Texto copiado para clipboard!")
            else:
                messagebox.showwarning("Aviso", "Nenhum texto para copiar")
        except Exception as e:
            logger.error(f"Erro ao copiar: {e}")
            messagebox.showerror("Erro", f"Erro ao copiar: {e}")

# ===== MAIN =====
if __name__ == "__main__":
    root = ctk.CTk()
    app = TranscriptorApp(root)
    root.mainloop()
