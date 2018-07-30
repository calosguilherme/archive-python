import os

def searchArqExtAllFolder(extensao,diretorio):              ##Varre todas as subpastas do diretorio informado
    arquivo=[]                                              ##E  retorna uma lista com todos os arquivos
    for root, dirs, files in os.walk(diretorio):            ##Encontrados com a extensão informada
        for file in files:
            if file.endswith(extensao):
                arquivo.append(os.path.join(root, file))
    return(arquivo)

def verificaomnetpp(linha):            ##Verificar se na linha possui algum dos prefixos do omnetpp abaixo
    prefi = ["connections:","connections allowunconnected:", "submodules:", "gates:"]
    for i in prefi:
        if(i in linha):
            return(True)
    return(False)

arquivos=[] ## Variavel para armazenar os arquivos que seram buscados os parametros
copia=False ## Variavel para controlar a leitura do arquivo, fica True assim que passa na linha parameters: onde começa a lista de parametros
temparametro=False ## Variavel para verificar se o arquivo possui algum parametro dentro do campo parameters: para evitar adicionar arquivo a lista onde não possui nenhum parametro
arquivos=searchArqExtAllFolder(".ned", "/omnetpp/_workspace/elastico/") ## Extensão Ned e raiz da pasta a ser varrida
newarq = open("/omnetpp/Lista_de_Parametros.ned", "w")   ## Nome do Arquivo que vai ser gerado

for i in arquivos: ##Loop para a leitura de conteudo de cada arquivo
    arq = open(i, 'r')
    texto = arq.readlines()
    copia=False
    for linha in texto : ##Loop para leitura de linha por linha de cada arquivo
        if(copia):
            if("@d" not in linha and linha != "\n" and  not verificaomnetpp(linha) and "}" not in linha and "{" not in linha and linha.strip()): ## If para não copiar os { } linhas vazias tag @display e outros prefixos como o parameters usado pelo omnetpp
                newarq.write(linha) ##Copia a linha para o arquivo novo
                temparametro=True
        if("parameters:" in linha): ## Libera a copia das linhas apartir da linha seguinte ao parameters:
            copia = True
        elif(verificaomnetpp(linha)): ## Detecta outro prefixo do omnetpp, signifa que o parameters: finalizou e bloqueia a copia de linhas
            copia = False
    if(temparametro):
        newarq.write(i + '\n')
    arq.close()
    temparametro=False
newarq.close()
print("Arquivo Criado Com Sucesso")

