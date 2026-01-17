import os
import time
import threading
import logging
import customtkinter as ctk
from urllib.parse import unquote, urlparse
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# --- CONFIGURAÇÃO VISUAL ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert("end", msg + '\n')
            self.text_widget.see("end")
            self.text_widget.configure(state='disabled')
        self.text_widget.after(0, append)

class InvestigatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DEUS CODE - UNIVERSAL HARVESTER V5")
        self.geometry("900x650")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.resume_event = threading.Event()
        self.driver = None 

        self.lbl_title = ctk.CTkLabel(self, text="CENTRAL DE EXTRAÇÃO UNIVERSAL", font=("Roboto", 22, "bold"))
        self.lbl_title.grid(row=0, column=0, padx=20, pady=(20, 5))

        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_url = ctk.CTkLabel(self.frame_config, text="URL Alvo:")
        self.lbl_url.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_url = ctk.CTkEntry(self.frame_config, width=500, placeholder_text="Cole o link do site (Repositório, Blog, Portal)...")
        self.entry_url.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        
        self.lbl_folder = ctk.CTkLabel(self.frame_config, text="Nome da Pasta:")
        self.lbl_folder.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_folder = ctk.CTkEntry(self.frame_config, width=200, placeholder_text="Ex: Manuais_Antigos_PDF")
        self.entry_folder.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.chk_deep = ctk.CTkCheckBox(self.frame_config, text="Modo Profundo (Deep Scan - Varrer Links)", text_color="orange")
        self.chk_deep.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.frame_controls = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_controls.grid(row=2, column=0, padx=20, pady=5)

        self.btn_start = ctk.CTkButton(self.frame_controls, text="ABRIR NAVEGADOR", command=self.start_thread, 
                                       fg_color="green", hover_color="darkgreen", height=40, font=("Roboto", 14, "bold"))
        self.btn_start.pack(side="left", padx=10)

        self.btn_resume = ctk.CTkButton(self.frame_controls, text="JÁ ESTOU LOGADO / CONTINUAR", command=self.resume_script,
                                        fg_color="gray", state="disabled", height=40, font=("Roboto", 12, "bold"))
        self.btn_resume.pack(side="left", padx=10)

        self.textbox_log = ctk.CTkTextbox(self, font=("Consolas", 12))
        self.textbox_log.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.textbox_log.configure(state='disabled')
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = TextHandler(self.textbox_log)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def start_thread(self):
        url = self.entry_url.get()
        folder_name = self.entry_folder.get()
        deep_mode = self.chk_deep.get()

        if not url:
            self.logger.error("ERRO: URL vazia!")
            return
        
        self.btn_start.configure(state="disabled", text="NAVEGADOR ABERTO")
        self.resume_event.clear()
        thread = threading.Thread(target=self.run_scraper, args=(url, folder_name, deep_mode))
        thread.start()

    def resume_script(self):
        self.logger.info(">>> LOGIN CONFIRMADO. INICIANDO EXTRAÇÃO... <<<")
        self.resume_event.set()

    def sanitizar_nome(self, nome):
        return nome.replace(":", "").replace("/", "").replace("\\", "").replace("?", "").replace("*", "")

    def run_scraper(self, target_url, custom_folder_name, deep_mode):
        try:
            self.logger.info(">>> INICIALIZANDO PROTOCOLO V5 (UNIVERSAL) <<<")
            
            base_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'INVESTIGACAO_DATA')
            if custom_folder_name:
                final_folder_name = self.sanitizar_nome(custom_folder_name)
            else:
                parsed = urlparse(target_url)
                final_folder_name = parsed.netloc.replace("www.", "").replace(".", "_")
            
            download_folder = os.path.join(base_folder, final_folder_name)
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            self.logger.info(f"Cofre Local: {download_folder}")
            self.driver = self.iniciar_navegador_stealth(download_folder)
            
            self.logger.info(f"Acessando: {target_url}")
            self.driver.get(target_url)

            self.logger.info("==========================================")
            self.logger.info("FAÇA O LOGIN MANUALMENTE (SE NECESSÁRIO).")
            self.logger.info("Depois clique em 'JÁ ESTOU LOGADO'.")
            self.logger.info("==========================================")
            
            self.btn_resume.configure(state="normal", fg_color="#1f538d")
            self.resume_event.wait()
            self.btn_resume.configure(state="disabled", fg_color="gray")

            self.logger.info("Mapeando links...")
            elementos = self.driver.find_elements(By.TAG_NAME, "a")
            alvos = []
            dominio = urlparse(target_url).netloc

            for elem in elementos:
                try:
                    href = elem.get_attribute("href")
                    if not href: continue
                    
                    if href.lower().endswith(".pdf"):
                        if href not in [x['url'] for x in alvos]:
                            alvos.append({'type': 'direct', 'url': href})
                    
                    elif deep_mode and dominio in href:
                        exclusoes = ['login', 'register', '#', 'javascript', 'logout', 'signin', 'assine', 'planos']
                        if not any(ex in href for ex in exclusoes):
                            if href not in [x['url'] for x in alvos]:
                                alvos.append({'type': 'page', 'url': href})
                except:
                    continue
            
            self.logger.info(f"Links potenciais: {len(alvos)}")
            
            if deep_mode and len(alvos) > 40:
                 alvos = alvos[:40]

            count = 0
            for i, item in enumerate(alvos):
                try:
                    _ = self.driver.window_handles
                except:
                    self.logger.error("Navegador fechado!")
                    break

                link = item['url']
                
                # --- LÓGICA DE DOWNLOAD DIRETO ---
                if item['type'] == 'direct':
                    nome = unquote(link.split("/")[-1])
                    self.logger.info(f"Baixando PDF [{i+1}]: {nome}")
                    self.driver.get(link)
                    time.sleep(3)
                    count += 1
                
                # --- LÓGICA DE PÁGINA PROFUNDA ---
                elif item['type'] == 'page':
                    self.logger.info(f"Investigando [{i+1}]: {link}")
                    self.driver.get(link)
                    time.sleep(1.5)
                    
                    try:
                        # Procura PDF ou Botão Download
                        pdf_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
                        if not pdf_links:
                             pdf_links = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Download') or contains(text(), 'Baixar') or contains(@class, 'download')]")

                        if pdf_links:
                            for pdf in pdf_links:
                                pdf_url = pdf.get_attribute("href")
                                if pdf_url and "login" not in pdf_url:
                                    nome = unquote(pdf_url.split("/")[-1])
                                    
                                    self.logger.info(f" -> TENTANDO BAIXAR: {nome}")
                                    self.driver.get(pdf_url)
                                    time.sleep(2.5)
                                    
                                    # --- DETECTOR DE BLOQUEIO GENÉRICO ---
                                    url_atual = self.driver.current_url.lower()
                                    if "assine" in url_atual or "planos" in url_atual or "paywall" in url_atual:
                                        self.logger.warning(" -> 🛑 BLOQUEADO (PAYWALL). Ignorando.")
                                        self.driver.back() 
                                    else:
                                        self.logger.info(" -> SUCESSO (Provável).")
                                        count += 1
                                    
                                    break 
                        else:
                            self.logger.warning(f" -> Nenhum arquivo visível.")
                    except:
                        self.logger.warning(f" -> Erro na página.")

            self.logger.info(f">>> FIM. {count} ARQUIVOS PROCESSADOS. <<<")
            
        except Exception as e:
            self.logger.error(f"ERRO: {e}")
        finally:
            self.btn_start.configure(state="normal", text="INICIAR NAVEGADOR")

    def iniciar_navegador_stealth(self, download_path):
        options = uc.ChromeOptions()
        profile_path = os.path.join(os.getcwd(), 'chrome_profile_stealth')
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
            
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument("--no-first-run")
        
        prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0
        }
        options.add_experimental_option("prefs", prefs)
        
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=138)
        return driver

if __name__ == "__main__":
    app = InvestigatorApp()
    app.mainloop()