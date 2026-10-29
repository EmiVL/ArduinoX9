import os
import shutil
import pyautogui
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Extensões padrão configuradas
EXTENSOES_PADRAO = {
    'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.img'],
    'Áudios': ['.mp3', '.wav', '.aac'],
    'Documentos': ['.doc', '.docx', '.pdf', '.txt', '.xlsx'],
    'Vídeos': ['.mp4', '.mkv', '.avi', '.mov'],
    'XML': ['.xml']
}

def organizar_diretorio(caminho_pasta, extensao_custom=None, pasta_custom=None):
    if not os.path.exists(caminho_pasta):
        return False, "O caminho especificado não existe."

    for arquivo in os.listdir(caminho_pasta):
        caminho_completo = os.path.join(caminho_pasta, arquivo)
        
        # Ignora se for uma pasta
        if os.path.isdir(caminho_completo):
            continue
        
        _, ext = os.path.splitext(arquivo)
        ext = ext.lower()
        subpasta = "Outros"

        # Verifica se corresponde à regra customizada do usuário
        if extensao_custom and pasta_custom and ext == extensao_custom.lower():
            subpasta = pasta_custom
        else:
            # Verifica as regras padrão
            for categoria, extensoes in EXTENSOES_PADRAO.items():
                if ext in extensoes:
                    subpasta = categoria
                    break

        # Cria a pasta de destino se não existir e move o arquivo
        pasta_destino = os.path.join(caminho_pasta, subpasta)
        os.makedirs(pasta_destino, exist_ok=True)
        shutil.move(caminho_completo, os.path.join(pasta_destino, arquivo))
        
    return True, "Arquivos organizados com sucesso!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organizar-geral', methods=['POST'])
def organizar_geral():
    dados = request.json
    caminho = dados.get('caminho')
    ext_custom = dados.get('extensao_custom')
    pasta_custom = dados.get('pasta_custom')
    
    sucesso, mensagem = organizar_diretorio(caminho, ext_custom, pasta_custom)
    return jsonify({'sucesso': sucesso, 'mensagem': mensagem})

@app.route('/organizar-desktop', methods=['POST'])
def organizar_desktop():
    dados = request.json
    tipo_organizacao = dados.get('tipo') # 'alfabetica' ou 'pastas'
    
    # Caminho dinâmico para a Área de Trabalho do usuário atual
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    
    if tipo_organizacao == 'pastas':
        sucesso, mensagem = organizar_diretorio(desktop_path)
        return jsonify({'sucesso': sucesso, 'mensagem': "Área de Trabalho organizada por pastas!"})
    
    elif tipo_organizacao == 'alfabetica':
        try:
            # Automação RPA na Área de Trabalho usando PyAutoGUI
            # Minimiza janelas para focar no Desktop
            pyautogui.hotkey('win', 'd')
            pyautogui.sleep(1)
            
            # Clica com o botão direito no fundo do Desktop
            # Posição central estimada na tela
            largura, altura = pyautogui.size()
            pyautogui.rightClick(largura // 2, altura // 2)
            pyautogui.sleep(0.5)
            
            # Atalhos do Windows para Classificar por -> Nome
            # Pressiona 'o' para Ordenar por e depois 'n' para Nome (varia conforme idioma do OS)
            pyautogui.press('o')
            pyautogui.sleep(0.2)
            pyautogui.press('n')
            
            return jsonify({'sucesso': True, 'mensagem': "Comando RPA de ordenação alfabética enviado à Área de Trabalho!"})
        except Exception as e:
            return jsonify({'sucesso': False, 'mensagem': f"Erro no processo RPA: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
