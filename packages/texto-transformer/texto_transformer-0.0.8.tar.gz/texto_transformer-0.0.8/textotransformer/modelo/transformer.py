# Import das bibliotecas.

# Biblioteca de logging
import logging  
# Biblioteca de aprendizado de máquina
from torch import nn 
import torch 
import numpy as np
from torch import Tensor, device
# Biblioteca do transformer
from transformers import AutoModel, AutoTokenizer, AutoConfig, T5Config, MT5Config
from transformers import BertModel, AlbertModel, DistilBertModel, RobertaModel, XLNetModel, GPT2Model
# Biblioteca de manipulação json
import json
# Biblioteca de tipos
from typing import List, Dict, Optional, Union
# Biblioteca de manipulação sistema
import os

# Bibliotecas próprias
from textotransformer.modelo.modeloargumentos import ModeloArgumentos
from textotransformer.modelo.modeloenum import AbordagemExtracaoEmbeddingsCamadas
from textotransformer.pln.pln import PLN

logger = logging.getLogger(__name__)

# Constantes da classe
PALAVRA_FORA_DO_VOCABULARIO = 1
PALAVRA_DENTRO_DO_VOCABULARIO = 0

class Transformer(nn.Module):
    '''
    Classe que encapsula a classe AutoModel da Huggingface para gerar embeddings de token, palavra, sentença ou texto.
    Carrega a classe correta, por exemplo BERT / RoBERTa etc.

    Parâmetros:
       `modelo_args' - Argumentos passados para o modelo Huggingface Transformers.
       `cache_dir` - Cache dir para Huggingface Transformers para armazenar/carregar modelos.
       `tokenizer_args` - Argumentos (chave, pares de valor) passados para o modelo Huggingface Tokenizer
       `tokenizer_name_or_path` - Nome ou caminho do tokenizer. Quando None, model_name_or_path é usado    
    '''

    def __init__(self, 
                modelo_args : ModeloArgumentos,                
                cache_dir: Optional[str] = None,
                tokenizer_args: Dict = {}, 
                tokenizer_name_or_path : str = None):
        
        # Inicializa o construtor da superclasse
        super(Transformer, self).__init__()
        
        # Define os argumentos do modelo
        self.modelo_args = modelo_args

        # Recupera o nome do modelo dos argumentos
        model_name_or_path = modelo_args.pretrained_model_name_or_path;
      
        # Recupera parâmetros do transformador dos argumentos e cria um dicionário para o AutoConfig
        model_args = {"output_attentions": modelo_args.output_attentions, 
                      "output_hidden_states": modelo_args.output_hidden_states}
    
        # Configuração do modelo        
        self.auto_config = AutoConfig.from_pretrained(model_name_or_path, 
                                                      **model_args, 
                                                      cache_dir=cache_dir)
        
        # Carrega o modelo
        self._carregar_modelo(model_name_or_path, 
                              self.auto_config, 
                              cache_dir)

        # Carrega o tokenizador
        self.auto_tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path if tokenizer_name_or_path is not None else  model_name_or_path, cache_dir=cache_dir, **tokenizer_args)
        
        # Se não possuir um token de preenchimento, adiciona um
        if self.auto_tokenizer.pad_token is None:
            self.auto_tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            self.auto_model.resize_token_embeddings(len(self.auto_tokenizer))

        # Se max_seq_length não foi especificado, tenta inferir do modelo
        if self.modelo_args.max_seq_len is None:
            if hasattr(self.auto_model, "config") and hasattr(self.auto_model.config, "max_position_embeddings") and hasattr(self.auto_tokenizer, "model_max_length"):
                self.modelo_args.max_seq_len = min(self.auto_model.config.max_position_embeddings,
                                                   self.auto_tokenizer.model_max_length)

        # Define a classe do tokenizador
        if tokenizer_name_or_path is not None:
            self.auto_model.config.tokenizer_class = self.auto_tokenizer.__class__.__name__


        # Define os tokens especiais e separadores 
        self.defineTokensEspeciais()
                           
        logger.info("Classe \"{}\" carregada: \"{}\".".format(self.__class__.__name__, modelo_args))

    # ============================   
    def __repr__(self):
        '''
        Retorna uma string com descrição do objeto.
        '''

        return "Classe (\"{}\") carregada com o modelo \"{}\", m AutoConfig \"{}\", Transformer \"{}\" e tokenizador: \"{}\".".format(self.__class__.__name__,
                                                                                                                                      self.modelo_args.pretrained_model_name_or_path,
                                                                                                                                      self.auto_config.__class__.__name__,
                                                                                                                                      self.auto_model.__class__.__name__,
                                                                                                                                      self.auto_tokenizer.__class__.__name__)
    # ============================   
    def defineTokensEspeciais(self):
        '''
        Define os tokens especiais e separadores considerando o modelo instânciado.
        
        # A maioria dos modelos a posição do token de início é 1 e o token separador é -1
        # Em alguns a posição do token de início é 0(não existe) e o token separador é -2 e o último <sep> é o token de classificação <CLS>
        '''
        
        # Verifica a instãncia do modelo.
        if isinstance(self.auto_model, BertModel):
            # Uma sentença simples: [CLS] X [SEP]
            # Um par de sentenças: [CLS] A [SEP] B [SEP]
            self.SEPARADOR_TOKEN = "##" # Caracteres que separa palavras fora do vocabulário segundo o Algoritmo WordPiece.
            self.TOKEN_INICIO = "[CLS]"
            self.POSICAO_TOKEN_INICIO = 1 # Posição do token válido do início da lista de tokens.
            self.TOKEN_FIM = "[SEP]"
            self.POSICAO_TOKEN_FINAL = -1 # Posição do token válido do final da lista de tokens.
            self.TOKEN_SEPARADOR = "[SEP]"
            self.TOKEN_CLASSIFICACAO = "[CLS]"
            self.TOKEN_PADDING = "[PAD]" # O token de padding.
            self.TOKEN_MASCARA = "[MASK]"
            self.TOKEN_DESCONHECIDO = "[UNK]"
            self.PADDING_SIDE = 1 # Define o lado que será realizado o preenchimento das lista de tokens. 0: esquerda, 1: direita.
            
        elif isinstance(self.auto_model, AlbertModel):
            # Uma sentença simples: [CLS] X [SEP]
            # Um par de sentenças: [CLS] A [SEP] B [SEP]
            self.SEPARADOR_TOKEN = "▁" # Caracteres que separa palavras fora do vocabulário segundo o Algoritmo SentencePiece.
            self.TOKEN_INICIO = "[CLS]"
            self.POSICAO_TOKEN_INICIO = 1 # Posição do token válido do início da lista de tokens.
            self.TOKEN_FIM = "[SEP]"
            self.POSICAO_TOKEN_FINAL = -1 # Posição do token válido do final da lista de tokens.
            self.TOKEN_SEPARADOR = "[SEP]"
            self.TOKEN_CLASSIFICACAO = "[CLS]"
            self.TOKEN_PADDING = "<pad>" # O token de padding.
            self.TOKEN_MASCARA = "[MASK]"
            self.TOKEN_DESCONHECIDO = "<unk>"
            self.PADDING_SIDE = 1 # Define o lado que será realizado o preenchimento das lista de tokens. 0: esquerda, 1: direita.
        
        elif isinstance(self.auto_model, DistilBertModel):
            # Uma sentença simples: [CLS] X [SEP]
            # Um par de sentenças: [CLS] A [SEP] B [SEP]
            self.SEPARADOR_TOKEN = "##" # Caracteres que separa palavras fora do vocabulário segundo o Algoritmo WordPiece.
            self.TOKEN_INICIO = "[CLS]"
            self.POSICAO_TOKEN_INICIO = 1 # Posição do token válido do início da lista de tokens.
            self.TOKEN_FIM = "[SEP]"
            self.POSICAO_TOKEN_FINAL = -1 # Posição do token válido do final da lista de tokens.
            self.TOKEN_SEPARADOR = "[SEP]"
            self.TOKEN_CLASSIFICACAO = "[CLS]"
            self.TOKEN_PADDING = "[PAD]" # O token de padding.
            self.TOKEN_MASCARA = "[MASK]"
            self.TOKEN_DESCONHECIDO = "<unk>"
            self.PADDING_SIDE = 1 # Define o lado que será realizado o preenchimento das lista de tokens. 0: esquerda, 1: direita.
        
        elif isinstance(self.auto_model, RobertaModel):
            # Uma sentença simples: <s> X </s>
            # Um par de sentenças: <s> A </s></s> B </s>
            self.SEPARADOR_TOKEN = "Ġ" # Caracter que separa palavras fora do vocabulário segundo o Algoritmo BPE.
            self.TOKEN_INICIO = "<s>"
            self.POSICAO_TOKEN_INICIO = 1 # Posição do token válido do início da lista de tokens.
            self.TOKEN_FIM = "</s>"
            self.POSICAO_TOKEN_FINAL = -1 # Posição do token válido do final da lista de tokens.
            self.TOKEN_SEPARADOR = "</s>"
            self.TOKEN_CLASSIFICACAO = "<s>"
            self.TOKEN_PADDING = "<pad>" # O token de padding.
            self.TOKEN_MASCARA = "<mask>"
            self.TOKEN_DESCONHECIDO = "Â"
            self.PADDING_SIDE = 1 # Define o lado que será realizado o preenchimento das lista de tokens. 0: esquerda, 1: direita.
            
        elif isinstance(self.auto_model, XLNetModel):
            # Uma sentença simples: X <sep> <cls>
            # Um par de sentenças: A <sep> B <sep> <cls>
            self.SEPARADOR_TOKEN = "▁"  # Caracter que separa palavras fora do vocabulário segundo o Algoritmo SentencePiece.
            self.TOKEN_INICIO = "<s>"
            # O token de início está no final da sentença junto como separador
            self.POSICAO_TOKEN_INICIO = 0 # Posição do token válido do início da lista de tokens.
            self.TOKEN_FIM = "</s>"
            self.POSICAO_TOKEN_FINAL = -2 # Posição do token válido do final da lista de tokens.
            self.TOKEN_SEPARADOR = "<sep>"
            self.TOKEN_CLASSIFICACAO = "<cls>"
            self.TOKEN_PADDING = "<pad>" # O token de padding.
            self.TOKEN_MASCARA = "<mask>"
            self.TOKEN_DESCONHECIDO = "<unk>"
            self.PADDING_SIDE = 0 # Define o lado que será realizado o preenchimento das lista de tokens. 0: esquerda, 1: direita.

        elif isinstance(self.auto_model, GPT2Model):
            # Uma sentença simples: X
            # Um par de sentenças: A ,B
            self.SEPARADOR_TOKEN = "Ġ" # Caracter que separa palavras fora do vocabulário segundo o Algoritmo BPE.
            self.TOKEN_INICIO = None  # Não existe token de início
            self.POSICAO_TOKEN_INICIO = None    # Não existe token de início
            self.TOKEN_FIM = None # Não existe token de fim
            self.POSICAO_TOKEN_FINAL = None # Não existe token de fim
            self.TOKEN_SEPARADOR = None
            self.TOKEN_CLASSIFICACAO = None
            self.TOKEN_PADDING = "[PAD]" # O token de padding.
            self.TOKEN_MASCARA = None
            self.TOKEN_DESCONHECIDO = None
            self.PADDING_SIDE = 0 # Define o lado que será realizado o preenchimento das lista de tokens. 0: esquerda, 1: direita.

        else:
            # Sem um modelo especificado
            self.SEPARADOR_TOKEN = None
            self.TOKEN_INICIO = None
            self.POSICAO_TOKEN_INICIO = None
            self.TOKEN_FIM = None
            self.POSICAO_TOKEN_FINAL = None
            self.TOKEN_SEPARADOR = None
            self.TOKEN_CLASSIFICACAO = None
            self.TOKEN_PADDING = None
            self.TOKEN_MASCARA = None
            self.TOKEN_DESCONHECIDO = None
            self.PADDING_SIDE = 1 # Define o lado que será realizado o preenchimento das lista de tokens. 0: esquerda, 1: direita.           
            
            logger.info("Não foi definido os tokens especiais para o modelo {}.".format(self.auto_model.__class__.__name__))
    
    # ============================ 
    def getPosicaoTokenInicio(self) -> int:
        '''
        Recupera a posição do token de início válido da lista de tokens.

        Retorna:
           Um inteiro com a posição do token de início válido da lista de tokens.
        '''
        
        return self.POSICAO_TOKEN_INICIO
    
    # ============================ 
    def getPosicaoTokenFinal(self) -> int:
        '''
        Recupera a posição do token de fim válido da lista de tokens.

        Retorna:
           Um inteiro com a posição do token de fim válido da lista de tokens.
        '''
        
        return self.POSICAO_TOKEN_FINAL
    
    # ============================   
    def _carregar_modelo(self,
                         model_name_or_path: str, 
                         config, 
                         cache_dir):
        '''
        Carrega o modelo transformer

        Parâmetros:
           `model_name_or_path` - Nome ou caminho do modelo.
           `config` - Configuração do modelo.
           `cache_dir` - Diretório de cache.
        '''

        # Carregamento T5
        if isinstance(config, T5Config):
            self._load_t5_model(model_name_or_path, 
                                config, 
                                cache_dir)
        
        else:
            # Carregamento MT5
            if isinstance(config, MT5Config):
                self._load_mt5_model(model_name_or_path, 
                                    config, 
                                    cache_dir)
            else:
                # Carrega modelos genéricos
                self.auto_model = AutoModel.from_pretrained(model_name_or_path, 
                                                            config=config, 
                                                            cache_dir=cache_dir)

    # ============================   
    def _load_t5_model(self, model_name_or_path: str, 
                       config, 
                       cache_dir):
        '''
        Carrega codificador do modelo¨T5

        Parâmetros:
           `model_name_or_path` - Nome ou caminho do modelo.
           `config` - Configuração do modelo.
           `cache_dir` - Diretório de cache.
        '''

        from transformers import T5EncoderModel
        T5EncoderModel._keys_to_ignore_on_load_unexpected = ["decoder.*"]
        self.auto_model = T5EncoderModel.from_pretrained(model_name_or_path, 
                                                         config=config, 
                                                         cache_dir=cache_dir)

    # ============================   
    def _load_mt5_model(self, model_name_or_path: str, 
                        config, 
                        cache_dir):
        '''
        Carrega codificador do modelo MT5

        Parâmetros:
           `model_name_or_path` - Nome ou caminho do modelo.
           `config` - Configuração do modelo.
           `cache_dir` - Diretório de cache.
        '''

        from transformers import MT5EncoderModel
        MT5EncoderModel._keys_to_ignore_on_load_unexpected = ["decoder.*"]
        self.auto_model = MT5EncoderModel.from_pretrained(model_name_or_path, 
                                                          config=config, 
                                                          cache_dir=cache_dir)
   
    # ============================      
    def getTextoTokenizado(self, texto : str,
                           addicionar_tokens_especiais: bool = True) -> List[str]:
        '''
        Retorna um texto tokenizado e concatenado com tokens especiais '[CLS]' no início e o token '[SEP]' no fim para ser submetido ao modelo de linguagem.
        
        Parâmetros:
           `texto` - Um texto a ser tokenizado.
        
        Retorno:
           `texto_tokenizado` - Texto tokenizado.
        '''

        # Tokeniza o texto
        saida = self.tokenize(texto, addicionar_tokens_especiais=addicionar_tokens_especiais)
        
        # Recupera o texto tokenizado da primeira posição, pois o texto vem em uma lista
        texto_tokenizado = saida['tokens_texto_mcl'][0]

        return texto_tokenizado

    # ============================    
    def removeTokensEspeciais(self, lista_tokens: List[str]) -> List[str]:
        '''
        Remove os tokens especiais de início, fim, separador e classificação  da lista de tokens.
        
        Parâmetros:
           `lista_tokens` - Uma lista de tokens.
        
        Retorno:
              Uma lista de tokens sem os tokens especiais.
        '''
        
        # Se possui token de início e faz parte da lista
        if self.TOKEN_INICIO != None and self.TOKEN_INICIO in lista_tokens:
             lista_tokens.remove(self.TOKEN_INICIO)
        else:
           logger.info("Não removi o token especial início (\"{}\") da lista de tokens: {}.".format(self.TOKEN_INICIO, lista_tokens))

        # Se possui token de início e faz parte da lista
        if self.TOKEN_FIM != None and self.TOKEN_FIM in lista_tokens:
             lista_tokens.remove(self.TOKEN_FIM)
        else:
           logger.info("Não removi o token especial fim (\"{}\") da lista de tokens: {}.".format(self.TOKEN_FIM, lista_tokens))

        # Se possui token de separação da lista
        if self.TOKEN_SEPARADOR != None and self.TOKEN_SEPARADOR in lista_tokens:
             lista_tokens.remove(self.TOKEN_SEPARADOR)
        else:
           logger.info("Não removi o token especial separador (\"{}\") da lista de tokens: {}.".format(self.TOKEN_SEPARADOR, lista_tokens))
           
        # Se possui token de separação da lista
        if self.TOKEN_CLASSIFICACAO != None and self.TOKEN_CLASSIFICACAO in lista_tokens:
             lista_tokens.remove(self.TOKEN_CLASSIFICACAO)
        else:
           logger.info("Não removi o token especial de classificação (\"{}\") da lista de tokens: {}.".format(self.TOKEN_CLASSIFICACAO, lista_tokens))           
            
        return lista_tokens

    # ============================ 
    def tokenize(self, texto: Union[str, List[str]],
                 addicionar_tokens_especiais: bool = True) -> dict:
        '''        
        Tokeniza um texto para submeter ao modelo de linguagem. 
        Retorna um dicionário listas de mesmo tamanho para garantir o processamento em lote.
        Use a quantidade de tokens para saber até onde deve ser recuperado em uma lista de saída.
        Ou use attention_mask diferente de 1 para saber que posições devem ser utilizadas na lista.

        Parâmetros:
           `texto` - Texto é uma string ou uma lista de strings a serem tokenizados para o modelo de linguagem.
           `addicionar_tokens_especiais` - Adiciona os tokens especiais de início e separação no texto.
                          
        Retorna um dicionário com as seguintes chaves:
           `tokens_texto_mcl` - Uma lista com os textos tokenizados com os tokens especiais.
           `input_ids` - Uma lsta com os ids dos tokens de entrada mapeados em seus índices do vocabuário.
           `token_type_ids` - Uma lista com os tipos dos tokens.
           `attention_mask` - Uma lista com os as máscaras de atenção indicando com '1' os tokens  pertencentes à sentença.
        '''
        
        # Dicionário com a saída do tokenizador
        saida = {}
        
        # Se o texto for uma string coloca em uma lista de listas para tokenizar
        if isinstance(texto, str):
            to_tokenize = [[texto]]
        else:
            # Se for uma lista de strings coloca em uma lista para tokenizar
            if isinstance(texto[0], str):
                to_tokenize = [texto]
            else:
                # Se for uma lista de listas de strings, não faz nada
                to_tokenize = texto
                
        # Remove os espaços em branco antes e depois de cada texto usando strip
        to_tokenize = [[str(s).strip() for s in col] for col in to_tokenize]

        # Se for para colocar para minúsculo usa Lowercase nos textos
        if self.modelo_args.do_lower_case:
            # Convertendo todos os tokens para minúsculo
            to_tokenize = [[s.lower() for s in col] for col in to_tokenize]

        # Tokeniza o texto
        # Faz o mesmo que o método encode_plus com uma string e o mesmo que batch_encode_plus com uma lista de strings.
        saida.update(self.auto_tokenizer(*to_tokenize,  # Texto a ser codificado. O '*' remove a lista de listas de to_tokenize.
                                         add_special_tokens=addicionar_tokens_especiais, # Adiciona os tokens especiais '[CLS]' e '[SEP]'.
                                         padding=True, # Preenche o texto até max_length.
                                         truncation='longest_first',  # Trunca o texto no maior texto.
                                         return_tensors="pt",  # Retorna os dados como tensores pytorch.
                                         max_length=self.modelo_args.max_seq_len # Define o tamanho máximo para preencheer ou truncar.
                                        ) 
                    )
                        
        # Gera o texto tokenizado convertendo os ids para os respectivos tokens           
        saida['tokens_texto_mcl'] = [[self.auto_tokenizer.convert_ids_to_tokens(s.item()) for s in col] for col in saida['input_ids']]

        # Guarda o texto original        
        saida['texto_original'] = [[s for s in col] for col in to_tokenize][0]     
        
        # Verifica se existe algum texto maior que o limite de tokenização
        for tokens in saida['tokens_texto_mcl']:
            if len(tokens) >= 512:
                logger.info("Utilizando embeddings do modelo de:\"{}\".".format(AbordagemExtracaoEmbeddingsCamadas.converteInt(self.modelo_args.abordagem_extracao_embeddings_camadas).getStr()))
  
        return saida
        
    # ============================           
    def getSaidaRede(self, texto: dict) -> dict:
        '''
        De um texto preparado(tokenizado) retorna os embeddings dos tokens do texto. 
        O retorno é um dicionário com token_embeddings, input_ids, attention_mask, token_type_ids, 
        tokens_texto_mcl, texto_original  e all_layer_embeddings.
        
        Retorna os embeddings de todas as camadas de um texto.
    
        Parâmetros:
           `texto` - Um texto tokenizado a ser recuperado os embeddings do modelo de linguagem
    
        Retorna um dicionário com as seguintes chaves:
           `token_embeddings` - Uma lista com os embeddings da última camada.
           `input_ids` - Uma lista com os textos indexados.            
           `attention_mask` - Uma lista com os as máscaras de atenção
           `token_type_ids` - Uma lista com os tipos dos tokens.            
           `tokens_texto_mcl` - Uma lista com os textos tokenizados com os tokens especiais.
           `texto_origina`l - Uma lista com os textos originais.
           `all_layer_embeddings` - Uma lista com os embeddings de todas as camadas.
        '''
    
        # Recupera o texto preparado pelo tokenizador para envio ao modelo
        dic_texto_tokenizado = {'input_ids': texto['input_ids'],                                 
                                'attention_mask': texto['attention_mask']}
        
        # Se token_type_ids estiver no texto preparado copia para dicionário tokenizado
        # Alguns modelos como o Roberta não utilizam token_type_ids
        if 'token_type_ids' in texto:
            dic_texto_tokenizado['token_type_ids'] = texto['token_type_ids']

        # Roda o texto através do modelo, e coleta todos os estados ocultos produzidos.
        outputs = self.auto_model(**dic_texto_tokenizado, 
                                  return_dict=False)
        
        # A avaliação do modelo retorna um número de diferentes objetos com base em
        # como é configurado na chamada do método `from_pretrained` anterior. Nesse caso,
        # porque definimos `output_hidden_states = True`, o terceiro item será o
        # estados ocultos(hidden_states) de todas as camadas. Veja a documentação para mais detalhes:
        # https://huggingface.co/transformers/model_doc/bert.html#bertmodel

        # Retorno de model quando ´output_hidden_states=True´ é setado:    
        # outputs[0] = last_hidden_state, outputs[1] = pooler_output, outputs[2] = hidden_states
        
        # hidden_states é uma lista python, e cada elemento um tensor pytorch no formado <lote> x <qtde_tokens> x <768 ou 1024>.        
        # 0-texto_tokenizado, 1-input_ids, 2-attention_mask, 3-token_type_ids, 4-outputs(0=last_hidden_state,1=pooler_output,2=hidden_states)
        
        # Recupera a última camada de embeddings da saida do modelo
        last_hidden_state = outputs[0]

        # Adiciona os embeddings da última camada e os dados do texto preparado na saída
        saida = {}
        saida.update({'token_embeddings': last_hidden_state,  # Embeddings da última camada
                      'input_ids': texto['input_ids'],
                      'attention_mask': texto['attention_mask'],
                      'tokens_texto_mcl': texto['tokens_texto_mcl'],
                      'texto_original': texto['texto_original']
                      }
                    )

        # Se output_hidden_states == True existem embeddings nas camadas ocultas
        if self.auto_model.config.output_hidden_states:
            # 2 é o índice da saída com todos os embeddings em outputs
            all_layer_idx = 2
            if len(outputs) < 3: #Alguns modelos apenas geram last_hidden_states e all_hidden_states
                all_layer_idx = 1

            # Recupera todos as camadas do transformer
            # Tuplas com cada uma das camadas
            hidden_states = outputs[all_layer_idx]
            
            # Adiciona os embeddings de todas as camadas na saída
            saida.update({'all_layer_embeddings': hidden_states})

        return saida

    # ============================
    def getEmbeddingPrimeiraCamadaRede(self, saida_rede: dict) -> list:
        '''
        Retorna os embeddings extraído da primeira camada do transformer.

        Parâmtros:
           `saida_rede` - Um dicionário com a saída da rede.

        Retorno:
           Uma lista com os embeddings.
        '''
        
        # Retorna toda a primeira(0) camada da saida da rede.
        # Entrada: List das camadas(13 ou 25) (<1(lote)> x <qtde_tokens> x <768 ou 1024>)          
        resultado = saida_rede['all_layer_embeddings'][0]
        # Retorno: (<1(lote)> x <qtde_tokens> x <768 ou 1024>)  
        #print('resultado=',resultado.size())

        return resultado

    # ============================
    def getEmbeddingPenultimaCamada(self, saida_rede: dict) -> list:
        '''
        Retorna os embeddings extraído da penúltima camada do transformer.
        
        Parâmtros:
           `saida_rede` - Um dicionário com a saída da rede.

        Retorno:
           Uma lista com os embeddings.
        '''
        # Retorna todas a penúltima(-2) camada
        # Entrada: List das camadas(13 ou 25) (<1(lote)> x <qtde_tokens> x <768 ou 1024>)  
        resultado = saida_rede['all_layer_embeddings'][-2]
        # Retorno: (<1(lote)> x <qtde_tokens> <768 ou 1024>)  
        #print('resultado=',resultado.size())

        return resultado

    # ============================
    def getEmbeddingUltimaCamada(self, saida_rede: dict) -> list:
        '''
        Retorna os embeddings extraído da última camada do transformer.
        
        Parâmtros:
           `saida_rede` - Um dicionário com a saída da rede.

        Retorno:
           Uma lista com os embeddings.
        '''
        # Retorna todas a última(-1) camada
        # Entrada: List das camadas(13 ou 25) (<1(lote)> x <qtde_tokens> x <768 ou 1024>)  
        resultado = saida_rede['all_layer_embeddings'][-1]
        # Retorno: (<1(lote)> x <qtde_tokens> <768 ou 1024>)  
        #print('resultado=',resultado.size())

        return resultado        

     # ============================
    def getEmbeddingSoma4UltimasCamadas(self, saida_rede: dict) -> list:
        '''        
        Retorna a soma dos embeddings extraído das 4 últimas camada do transformer.
     
        Parâmtros:
           `saida_rede` - Um dicionário com a saída da rede.

        Retorno:
           Uma lista com os embeddings.
        '''
        
        # Retorna todas as 4 últimas camadas
        # Entrada: List das camadas(13 ou 25) (<1(lote)> x <qtde_tokens> <768 ou 1024>)  
        embedding_camadas = saida_rede['all_layer_embeddings'][-4:]
        # Retorno: List das camadas(4) (<1(lote)> x <qtde_tokens> x <768 ou 1024>)  

        # Usa o método `stack` para criar uma nova dimensão no tensor 
        # com a concateção dos tensores dos embeddings.        
        # Entrada: List das camadas(4) (<1(lote)> x <qtde_tokens> <768 ou 1024>)  
        resultado_stack = torch.stack(embedding_camadas, dim=0)
        # Retorno: <4> x <1(lote)> x <qtde_tokens> x <768 ou 1024>
        #print('resultado_stack=',resultado_stack.size())
      
        # Realiza a soma dos embeddings de todos os tokens para as camadas
        # Entrada: <4> x <1(lote)> x <qtde_tokens> x <768 ou 1024>
        resultado = torch.sum(resultado_stack, dim=0)
        # Saida: <1(lote)> x <qtde_tokens> x <768 ou 1024>
        #print('resultado=',resultado.size())

        return resultado

    # ============================
    def getEmbeddingConcat4UltimasCamadas(self, saida_rede: dict) -> list:
        '''        
        Retorna a concatenação dos embeddings das 4 últimas camadas do transformer.
             
        Parâmtros:
           `saida_rede` - Um dicionário com a saída da rede.

        Retorno:
           Uma lista com os embeddings.
        '''
        
        # Cria uma lista com os tensores a serem concatenados
        # Entrada: List das camadas(13 ou 25) (<1(lote)> x <qtde_tokens> x <768 ou 1024>)  
        # Lista com os tensores a serem concatenados
        lista_concatenada = []
        
        # Percorre os 4 últimos tensores da lista(camadas)
        for i in [-1, -2, -3, -4]:
            # Concatena da lista
            lista_concatenada.append(saida_rede['all_layer_embeddings'][i])
            
        # Retorno: Entrada: List das camadas(4) (<1(lote)> x <qtde_tokens> <768 ou 1024>)  
        #print('lista_concatenada=',len(lista_concatenada))

        # Realiza a concatenação dos embeddings de todos as camadas
        # Retorno: Entrada: List das camadas(4) (<1(lote)> x <qtde_tokens> <768 ou 1024>)  
        resultado = torch.cat(lista_concatenada, dim=-1)
        # Retorno: Entrada: (<1(lote)> x <qtde_tokens> <3072 ou 4096>)  
        # print('resultado=',resultado.size())
      
        return resultado

    # ============================
    def getEmbeddingSomaTodasAsCamada(self, saida_rede: dict) -> list:
        '''
        Retorna a soma dos embeddings extraído de todas as camadas do transformer.
                   
        Parâmtros:
           `saida_rede` - Um dicionário com a saída da rede.

        Retorno:
           Uma lista com os embeddings.
        '''
      
        # Retorna todas as camadas descontando a primeira(0)
        # Entrada: List das camadas(13 ou 25) (<1(lote)> x <qtde_tokens> x <768 ou 1024>)  
        embedding_camadas = saida_rede['all_layer_embeddings'][1:]
        # Retorno: List das camadas(12 ou 24) (<1(lote)> x <qtde_tokens> <768 ou 1024>)  

        # Usa o método `stack` para criar uma nova dimensão no tensor 
        # com a concateção dos tensores dos embeddings.        
        # Entrada: List das camadas(12 ou 24) (<1(lote)> x <qtde_tokens> x <768 ou 1024>)  
        resultado_stack = torch.stack(embedding_camadas, dim=0)
        # Retorno: <12 ou 24> x <1(lote)> x <qtde_tokens> x <768 ou 1024>
        #print('resultado_stack=',resultado_stack.size())
      
        # Realiza a soma dos embeddings de todos os tokens para as camadas
        # Entrada: <12 ou 24> x <1(lote)> x <qtde_tokens> x <768 ou 1024>
        resultado = torch.sum(resultado_stack, dim=0)
        # Saida: <1(lote)> x <qtde_tokens> x <768 ou 1024>
        # print('resultado=',resultado.size())
      
        return resultado

    # ============================
    def getSaidaRedeCamada(self, texto: Union[str, dict], 
                           abordagem_extracao_embeddings_camadas: Union[int, AbordagemExtracaoEmbeddingsCamadas] = AbordagemExtracaoEmbeddingsCamadas.ULTIMA_CAMADA) -> dict:
        '''
        Retorna os embeddings do texto de acordo com a abordagem de extração especificada.
        
        Parâmetros:
           `texto` - Texto a ser recuperado os embeddings.
           `abordagem_extracao_embeddings_camadas` - Camada de onde deve ser recupera os embeddings.

        Retorno:
           Os embeddings da camada para o texto.
        '''
                
        # Verifica o tipo de dado do parâmetro 'abordagem_extracao_embeddings_camadas'
        if isinstance(abordagem_extracao_embeddings_camadas, int):
            
            # Converte o parâmetro estrategia_pooling para um objeto da classe AbordagemExtracaoEmbeddingsCamadas
            abordagem_extracao_embeddings_camadas = AbordagemExtracaoEmbeddingsCamadas.converteInt(abordagem_extracao_embeddings_camadas)
        
        # Recupera todos os embeddings da rede('all_layer_embeddings')
        saida_rede = self.getSaidaRede(texto)
                
        # Embedding extraído usando a abordagem de extração
        embedding_extraido_abordagem = None

        # Chama o método que recupera os embeddings da camada especificada
        if abordagem_extracao_embeddings_camadas == AbordagemExtracaoEmbeddingsCamadas.PRIMEIRA_CAMADA:
          embedding_extraido_abordagem = self.getEmbeddingPrimeiraCamadaRede(saida_rede)
        else:
            if abordagem_extracao_embeddings_camadas == AbordagemExtracaoEmbeddingsCamadas.PENULTIMA_CAMADA:
              embedding_extraido_abordagem = self.getEmbeddingPenultimaCamada(saida_rede)
            else:
                if abordagem_extracao_embeddings_camadas == AbordagemExtracaoEmbeddingsCamadas.ULTIMA_CAMADA:
                  embedding_extraido_abordagem = self.getEmbeddingUltimaCamada(saida_rede)
                else:
                    if abordagem_extracao_embeddings_camadas == AbordagemExtracaoEmbeddingsCamadas.SOMA_4_ULTIMAS_CAMADAS:
                      embedding_extraido_abordagem = self.getEmbeddingSoma4UltimasCamadas(saida_rede)
                    else:
                        if abordagem_extracao_embeddings_camadas == AbordagemExtracaoEmbeddingsCamadas.CONCAT_4_ULTIMAS_CAMADAS:
                            embedding_extraido_abordagem = self.getEmbeddingConcat4UltimasCamadas(saida_rede)
                        else:
                            if abordagem_extracao_embeddings_camadas == AbordagemExtracaoEmbeddingsCamadas.TODAS_AS_CAMADAS:
                                embedding_extraido_abordagem = self.getEmbeddingSomaTodasAsCamada(saida_rede)
                            else:                                
                                logger.error("Não foi especificado uma abordagem de extração dos embeddings das camadas do transformer.") 
        
        # Verifica se foi realizado a extração
        if embedding_extraido_abordagem != None:
          # Atualiza a saída com os embeddings extraídos usando abordagem
          saida_rede.update({'embedding_extraido': embedding_extraido_abordagem,  # Embeddings extraídos usando abordagem de extração
                             'abordagem_extracao_embeddings_camadas': abordagem_extracao_embeddings_camadas})  # Tipo da abordagem da extração  dos embeddings
        else:
          logger.error("Não foi especificado uma abordagem de extração dos embeddings das camadas do transformer.") 
          saida_rede = None  

        return saida_rede


    # ============================  
    def getTokensPalavrasEmbeddingsTexto(self, 
                                         embeddings_texto, 
                                         tokens_texto_mcl: list[str],
                                         tokens_texto_concatenado: str,
                                         pln: PLN,
                                         dic_excecao_maior:dict = {"":-1,},
                                         dic_excecao_menor:dict = {"1°":1,}) -> dict:
        '''
        Escolhe o melhor tokenizador de palavra para o texto de acordo com o modelo de linguagem.
        
        De um texto preparado(tokenizado) ou não, retorna os embeddings das palavras do texto. 
        Retorna 5 listas, os tokens(palavras), as postagging, tokens OOV, e os embeddings dos tokens igualando a quantidade de tokens do spaCy com a tokenização do MCL de acordo com a estratégia. 
        Utiliza duas estratégias para realizar o pooling de tokens que forma uma palavra.
            - Estratégia MEAN para calcular a média dos embeddings dos tokens que formam uma palavra.
            - Estratégia MAX para calcular o valor máximo dos embeddings dos tokens que formam uma palavra.
            
        Parâmetros:
           `texto` - Um texto a ser recuperado os embeddings das palavras do modelo de linguagem
           `embeddings_texto` - Os embeddings do texto gerados pelo método getEmbeddingsTexto
           `tokens_texto_mcl` - Os tokens do texto gerados pelo método getEmbeddingsTexto
           `tokens_texto_concatenado` - Os tokens do texto concatenado gerados pelo método getEmbeddingsTexto
           `pln` - Uma instância da classe PLN para realizar a tokenização e POS-Tagging do texto.
           `dic_excecao_maior` - Um dicionário de tokens de exceções e seus deslocamentos para considerar mais tokens do modelo de linguagem em relação ao spaCy.
           `dic_excecao_menor` = Um dicionário de tokens de exceções e seus deslocamentos para considerar menos tokens do modelo de linguagem em relação ao spaCy.
               
        Retorna um dicionário com as seguintes chaves: 
           `tokens_texto` - Uma lista com os tokens do texto gerados pelo método.
           `pos_texto_pln` - Uma lista com as postagging dos tokens gerados pela ferramenta de pln.
           `tokens_oov_texto_mcl` - Uma lista com os tokens OOV do mcl.
           `palavra_embeddings_MEAN` - Uma lista dos embeddings de palavras com a média dos embeddings(Estratégia MEAN) dos tokens que formam a palavra.
           `palavra_embeddings_MAX` - Uma lista dos embeddings de palavras com o máximo dos embeddings(Estratégia MAX) dos tokens que formam a palavra.
        ''' 
        
        # Tokenização Wordpiece (Separador, ##) para BERT, DistilBert
        if isinstance(self.auto_model, (BertModel, DistilBertModel)):
            return self.getTokensPalavrasEmbeddingsTextoWordPiece(embeddings_texto = embeddings_texto,
                                                                  tokens_texto_mcl = tokens_texto_mcl,
                                                                  tokens_texto_concatenado = tokens_texto_concatenado,
                                                                  pln = pln,
                                                                  dic_excecao_maior = dic_excecao_maior,
                                                                  dic_excecao_menor = dic_excecao_menor)
        else:
            # Tokenização SentencePiece (Separador, _) Albert, XLNet
            if isinstance(self.auto_model, (AlbertModel, XLNetModel)):
                return self.getTokensPalavrasEmbeddingsTextoSentencePiece(embeddings_texto = embeddings_texto,
                                                                          tokens_texto_mcl = tokens_texto_mcl,
                                                                          tokens_texto_concatenado = tokens_texto_concatenado,
                                                                          pln = pln,
                                                                          dic_excecao_maior = dic_excecao_maior,
                                                                          dic_excecao_menor = dic_excecao_menor)
            else:
                # Tokenização BPE (Separador, Ġ) para o Roberta e GPT2
                if isinstance(self.auto_model, (RobertaModel, GPT2Model)):
                    return self.getTokensPalavrasEmbeddingsTextoBPE(embeddings_texto = embeddings_texto,
                                                                    tokens_texto_mcl = tokens_texto_mcl,
                                                                    tokens_texto_concatenado = tokens_texto_concatenado,
                                                                    pln = pln,
                                                                    dic_excecao_maior = dic_excecao_maior,
                                                                    dic_excecao_menor = dic_excecao_menor)                    
                else:
                    logger.error("Não encontrei um tokenizador de palavras para o modelo {}.".format(self.auto_model)) 
                    return  None 


    def _inicializaDicionarioExcecao(self,
                                     dic_excecao_maior = None, 
                                     dic_excecao_menor = None):
        
        # Dicionário de tokens de exceções e seus deslocamentos para considerar mais tokens do modelo de linguagem em relação ao spaCy
        # A tokenização do modelo de linguagem gera mais tokens que a tokenização das palavras do spaCy
        #self._dic_excecao_maior = {"":-1,
        #                    }
        self._dic_excecao_maior = dic_excecao_maior
        
        # Dicionário de tokens de exceções e seus deslocamentos para considerar menos tokens do modelo de linguagem em relação ao spaCy
        # A tokenização do modelo de linguagem gera menos tokens que a tokenização das palavras do spaCy
        #self._dic_excecao_menor = {"1°":1,
        #                  }
        self._dic_excecao_menor = dic_excecao_menor
        
                             
    def _getExcecaoDicMaior(self, token: str):   
        '''
        Retorna o deslocamento do token no texto para considerar mais tokens do MCL em relação ao spaCy.

        Parâmetros:
           `token` - Um token a ser verificado se é uma exceção.

        Retorno:
           O deslocamento do token no texto para considerar mais tokens do MCL em relação ao spaCy.
        '''
    
        valor = self._dic_excecao_maior.get(token)
        if valor != None:
            return valor
        else:
            return -1                             
    
    def _getExcecaoDicMenor(self, token: str): 
        '''
        Retorna o deslocamento do token no texto para considerar menos tokens do MCL em relação ao spaCy.

        Parâmetros:
           `token` - Um token a ser verificado se é uma exceção.

        Retorno:
           O deslocamento do token no texto para considerar menos tokens do MCL em relação ao spaCy.
        '''  
        
        valor = self._dic_excecao_menor.get(token)
        if valor != None:
            return valor
        else:
            return -1
                        
    # ============================  
    # getTokensPalavrasEmbeddingsTextoWordPiece
    # Gera os tokens, POS e embeddings de cada texto.
    
    def getTokensPalavrasEmbeddingsTextoWordPiece(self,
                                                  embeddings_texto,
                                                  tokens_texto_mcl: list[str],
                                                  tokens_texto_concatenado: str,
                                                  pln: PLN,
                                                  dic_excecao_maior:dict = {"":-1,},
                                                  dic_excecao_menor:dict = {"1°":1,}) -> dict:
        '''
        De um texto preparado(tokenizado) ou não, retorna os embeddings das palavras do texto. 
        Retorna 5 listas, os tokens(palavras), as postagging, tokens OOV, e os embeddings dos tokens igualando a quantidade de tokens do spaCy com a tokenização do MCL de acordo com a estratégia. 
        Utiliza duas estratégias para realizar o pooling de tokens que forma uma palavra.
            - Estratégia MEAN para calcular a média dos embeddings dos tokens que formam uma palavra.
            - Estratégia MAX para calcular o valor máximo dos embeddings dos tokens que formam uma palavra.
            
        Parâmetros:
           `texto` - Um texto a ser recuperado os embeddings das palavras do modelo de linguagem
           `embeddings_texto` - Os embeddings do texto gerados pelo método getEmbeddingsTexto
           `tokens_texto_mcl` - Os tokens do texto gerados pelo método getEmbeddingsTexto
           `tokens_texto_concatenado` - Os tokens do texto concatenado gerados pelo método getEmbeddingsTexto
           `pln` - Uma instância da classe PLN para realizar a tokenização e POS-Tagging do texto.
           `dic_excecao_maior` - Um dicionário de tokens de exceções e seus deslocamentos para considerar mais tokens do modelo de linguagem em relação ao spaCy.
           `dic_excecao_menor` = Um dicionário de tokens de exceções e seus deslocamentos para considerar menos tokens do modelo de linguagem em relação ao spaCy.
               
        Retorna um dicionário com as seguintes chaves: 
           `tokens_texto` - Uma lista com os tokens do texto gerados pelo método.
           `pos_texto_pln` - Uma lista com as postagging dos tokens gerados pela ferramenta de pln.
           `tokens_oov_texto_mcl` - Uma lista com os tokens OOV do mcl.
           `palavra_embeddings_MEAN` - Uma lista dos embeddings de palavras com a média dos embeddings(Estratégia MEAN) dos tokens que formam a palavra.
           `palavra_embeddings_MAX` - Uma lista dos embeddings de palavras com o máximo dos embeddings(Estratégia MAX) dos tokens que formam a palavra.
        '''
        
        # Inicializa os dicionários de exceção
        self._inicializaDicionarioExcecao(dic_excecao_maior, dic_excecao_menor)
       
        # Constantes tokens especiais
        #self.SEPARADOR_TOKEN = "##"
        #self.TOKEN_DESCONHECIDO = "[UNK]"
       
        # Guarda os tokens e embeddings de retorno
        lista_tokens = []
        lista_tokens_oov_mcl = []
        lista_palavra_embeddings_MEAN = []
        lista_palavra_embeddings_MAX = []
        
        # Gera a tokenização e POS-Tagging da sentença    
        lista_tokens_texto_pln, lista_pos_texto_pln = pln.getListaTokensPOSTexto(tokens_texto_concatenado)

        # print("\tokens_texto_concatenado    :",tokens_texto_concatenado)    
        # print("lista_tokens_texto_pln       :",lista_tokens_texto_pln)
        # print("len(lista_tokens_texto_pln)  :",len(lista_tokens_texto_pln))    
        # print("lista_pos_texto_pln          :",lista_pos_texto_pln)
        # print("len(lista_pos_texto_pln)     :",len(lista_pos_texto_pln))
        
        # embedding <qtde_tokens x 4096>        
        # print("embeddings_texto          :",embeddings_texto.shape)
        # print("tokens_texto_mcl          :",tokens_texto_mcl)
        # print("len(tokens_texto_mcl)     :",len(tokens_texto_mcl))

        # Seleciona os pares de palavra a serem avaliadas
        pos_wi = 0 # Posição do token da palavra gerado pelo spaCy
        pos_wj = pos_wi # Posição do token da palavra gerado pelo MCL
        pos2 = -1

        # Enquanto o indíce da palavra pos_wj(2a palavra) não chegou ao final da quantidade de tokens do MCL
        while (pos_wj < len(tokens_texto_mcl)):  

            # Seleciona os tokens da sentença
            wi = lista_tokens_texto_pln[pos_wi] # Recupera o token da palavra gerado pelo spaCy
            wi1 = ""
            pos2 = -1
            if pos_wi+1 < len(lista_tokens_texto_pln):
                wi1 = lista_tokens_texto_pln[pos_wi+1] # Recupera o próximo token da palavra gerado pelo spaCy
      
                # Localiza o deslocamento da exceção        
                pos2 = self._getExcecaoDicMenor(wi+wi1)  
                #print("Exceção pos2:", pos2)

            wj = tokens_texto_mcl[pos_wj] # Recupera o token da palavra gerado pelo MCL
            # print("wi[",pos_wi,"]=", wi)
            # print("wj[",pos_wj,"]=", wj)

            # Tratando exceções
            # Localiza o deslocamento da exceção
            pos = self._getExcecaoDicMaior(wi)  
            #print("Exceção pos:", pos)
                
            if (pos != -1) or (pos2 != -1):      
                if pos != -1:
                    #print("Adiciona 1 Exceção palavra == wi:", wi)
                    lista_tokens.append(wi)
                    # Marca como fora do vocabulário do MCL
                    lista_tokens_oov_mcl.append(PALAVRA_FORA_DO_VOCABULARIO)
                    # Verifica se tem mais de um token
                    if pos != 1:
                        indice_token = pos_wj + pos
                        #print("Calcula a média de :", pos_wj , "até", indice_token)
                        embeddings_tokens_palavra = embeddings_texto[pos_wj:indice_token]
                        #print("embeddings_tokens_palavra:",embeddings_tokens_palavra.shape)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular a média dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MEAN = torch.mean(embeddings_tokens_palavra, dim=0)
                        else:
                            embedding_estrategia_MEAN = np.mean(embeddings_tokens_palavra, axis=0)
                            
                        #print("embedding_estrategia_MEAN:",embedding_estrategia_MEAN.shape)
                        lista_palavra_embeddings_MEAN.append(embedding_estrategia_MEAN)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular o máximo dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MAX, linha = torch.max(embeddings_tokens_palavra, dim=0)
                        else:
                            embedding_estrategia_MAX, linha = np.max(embeddings_tokens_palavra, axis=0)
                        
                        #print("embedding_estrategia_MAX:",embedding_estrategia_MAX.shape)
                        lista_palavra_embeddings_MAX.append(embedding_estrategia_MAX)
                    else:
                        # Adiciona o embedding do token a lista de embeddings
                        lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])            
                        lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
             
                    # Avança para a próxima palavra e token do MCL
                    pos_wi = pos_wi + 1
                    pos_wj = pos_wj + pos
                    #print("Proxima:")            
                    #print("wi[",pos_wi,"]=", texto_token[pos_wi])
                    #print("wj[",pos_wj,"]=", texto_tokenizada_MCL[pos_wj])
                else:
                    if (pos2 != -1):
                        #print("Adiciona 1 Exceção palavra == wi:", wi)
                        lista_tokens.append(wi+wi1)
                        # Marca como fora do vocabulário do MCL
                        lista_tokens_oov_mcl.append(PALAVRA_FORA_DO_VOCABULARIO)
                        # Verifica se tem mais de um token
                        if (pos2 == 1): 
                            # Adiciona o embedding do token a lista de embeddings
                            lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])
                            lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
              
                        # Avança para a próxima palavra e token do MCL
                        pos_wi = pos_wi + 2
                        pos_wj = pos_wj + pos2
                        #print("Proxima:")            
                        #print("wi[",pos_wi,"]=", texto_token[pos_wi])
                        #print("wj[",pos_wj,"]=", texto_tokenizada_MCL[pos_wj])
            else:  
                # Tokens iguais adiciona a lista, o token não possui subtoken
                if (wi == wj) or (wj == self.TOKEN_DESCONHECIDO):
                    # Adiciona o token a lista de tokens
                    #print("Adiciona 2 wi==wj or wj==TOKEN_DESCONHECIDO:", wi)
                    lista_tokens.append(wi)    
                    # Marca como dentro do vocabulário do MCL
                    lista_tokens_oov_mcl.append(PALAVRA_DENTRO_DO_VOCABULARIO)
                    # Adiciona o embedding do token a lista de embeddings
                    lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])
                    lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
                    #print("embedding1[pos_wj]:", embedding_texto[pos_wj].shape)
                    # Avança para a próxima palavra e token do MCL
                    pos_wi = pos_wi + 1
                    pos_wj = pos_wj + 1   
                  
                else:          
                    # A palavra foi tokenizada pelo Wordpice com ## ou diferente do spaCy ou desconhecida
                    # Inicializa a palavra a ser montada          
                    palavra_POS = wj
                    indice_token = pos_wj + 1                 
                    while  (palavra_POS != wi) and (indice_token < len(tokens_texto_mcl)):
                        if (self.SEPARADOR_TOKEN != None) and (self.SEPARADOR_TOKEN in tokens_texto_mcl[indice_token]):
                            # Remove os caracteres SEPARADOR_PALAVRA("##") do token
                            parte = tokens_texto_mcl[indice_token][2:]
                        else:                
                            parte = tokens_texto_mcl[indice_token]
                  
                        palavra_POS = palavra_POS + parte
                        #print("palavra_POS:",palavra_POS)
                        # Avança para o próximo token do MCL
                        indice_token = indice_token + 1

                    #print("\nMontei palavra:",palavra_POS)
                    if (palavra_POS == wi) or (palavra_POS == self.TOKEN_DESCONHECIDO):
                        # Adiciona o token a lista
                        #print("Adiciona 3 palavra == wi or palavra_POS = TOKEN_DESCONHECIDO:",wi)
                        lista_tokens.append(wi)
                        # Marca como fora do vocabulário do MCL
                        lista_tokens_oov_mcl.append(PALAVRA_FORA_DO_VOCABULARIO)
                        # Calcula a média dos tokens da palavra
                        #print("Calcula o máximo :", pos_wj , "até", indice_token)
                        embeddings_tokens_palavra = embeddings_texto[pos_wj:indice_token]
                        #print("embeddings_tokens_palavra2:",embeddings_tokens_palavra)
                        #print("embeddings_tokens_palavra2:",embeddings_tokens_palavra.shape)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular a média dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MEAN = torch.mean(embeddings_tokens_palavra, dim=0)
                            #print("embedding_estrategia_MEAN:",embedding_estrategia_MEAN)
                            #print("embedding_estrategia_MEAN.shape:",embedding_estrategia_MEAN.shape)      
                        else:
                            embedding_estrategia_MEAN = np.mean(embeddings_tokens_palavra, axis=0)      
                              
                        lista_palavra_embeddings_MEAN.append(embedding_estrategia_MEAN)
                 
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular o valor máximo dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MAX, linha = torch.max(embeddings_tokens_palavra, dim=0)
                            #print("embedding_estrategia_MAX:",embedding_estrategia_MAX)
                            #print("embedding_estrategia_MAX.shape:",embedding_estrategia_MAX.shape)     
                        else:
                             embedding_estrategia_MAX = np.max(embeddings_tokens_palavra, axis=0)
                            
                        lista_palavra_embeddings_MAX.append(embedding_estrategia_MAX)

                    # Avança para o próximo token do spaCy
                    pos_wi = pos_wi + 1
                    # Pula para o próximo token do MCL
                    pos_wj = indice_token
        
        # Verificação se as listas estão com o mesmo tamanho
        if (len(lista_tokens) !=  len(lista_tokens_texto_pln)):
            logger.error("Erro na execução do método getTokensPalavrasEmbeddingsTextoWordPiece.")
            logger.error("texto                      :{}.".format(tokens_texto_concatenado))            
            logger.error("texto_token_pln            :{}.".format(lista_tokens_texto_pln))
            logger.error("lista_pos_texto_pln        :{}.".format(lista_pos_texto_pln))
            logger.error("texto_tokenizado_mcl       :{}.".format(tokens_texto_mcl))
            logger.error("lista_tokens               :{}.".format(lista_tokens))
            logger.error("len(lista_tokens)          :{}.".format(len(lista_tokens)))
            logger.error("lista_embeddings_MEAN      :{}.".format(lista_palavra_embeddings_MEAN))
            logger.error("len(lista_embeddings_MEAN) :{}.".format(len(lista_palavra_embeddings_MEAN)))
            logger.error("lista_embeddings_MAX       :{}.".format(lista_palavra_embeddings_MAX))
            logger.error("len(lista_embeddings_MAX)  :{}.".format(len(lista_palavra_embeddings_MAX)))
       
        # Remove as variáveis que não serão mais utilizadas
        del embeddings_texto
        del tokens_texto_mcl
        del lista_tokens_texto_pln

        # Retorna os tokens de palavras e os embeddings em um dicionário
        saida = {}
        saida.update({'tokens_texto' : lista_tokens,
                      'pos_texto_pln' : lista_pos_texto_pln,
                      'tokens_oov_texto_mcl' : lista_tokens_oov_mcl,
                      'palavra_embeddings_MEAN' : lista_palavra_embeddings_MEAN,
                      'palavra_embeddings_MAX' : lista_palavra_embeddings_MAX})

        return saida


    # ============================  
    # getTokensPalavrasEmbeddingsTextoSentencePiece(Albert)
    # Gera os tokens, POS e embeddings de cada texto.
    def getTokensPalavrasEmbeddingsTextoSentencePiece(self,
                                                      embeddings_texto, 
                                                      tokens_texto_mcl: list[str],
                                                      tokens_texto_concatenado: str,
                                                      pln: PLN,
                                                      dic_excecao_maior:dict = {"":-1,},
                                                      dic_excecao_menor:dict = {"1°":1,}) -> dict:
        '''
        De um texto preparado(tokenizado) ou não, retorna os embeddings das palavras do texto. 
        Retorna 5 listas, os tokens(palavras), as postagging, tokens OOV, e os embeddings dos tokens igualando a quantidade de tokens do spaCy com a tokenização do MCL de acordo com a estratégia. 
        Utiliza duas estratégias para realizar o pooling de tokens que forma uma palavra.
            - Estratégia MEAN para calcular a média dos embeddings dos tokens que formam uma palavra.
            - Estratégia MAX para calcular o valor máximo dos embeddings dos tokens que formam uma palavra.
            
        Parâmetros:
           `texto` - Um texto a ser recuperado os embeddings das palavras do modelo de linguagem
           `embeddings_texto` - Os embeddings do texto gerados pelo método getEmbeddingsTexto
           `tokens_texto_mcl` - Os tokens do texto gerados pelo método getEmbeddingsTexto
           `tokens_texto_concatenado` - Os tokens do texto concatenado gerados pelo método getEmbeddingsTexto
           `pln` - Uma instância da classe PLN para realizar a tokenização e POS-Tagging do texto.
           `dic_excecao_maior` - Um dicionário de tokens de exceções e seus deslocamentos para considerar mais tokens do modelo de linguagem em relação ao spaCy.
           `dic_excecao_menor` = Um dicionário de tokens de exceções e seus deslocamentos para considerar menos tokens do modelo de linguagem em relação ao spaCy.
               
        Retorna um dicionário com as seguintes chaves: 
           `tokens_texto` - Uma lista com os tokens do texto gerados pelo método.
           `pos_texto_pln` - Uma lista com as postagging dos tokens gerados pela ferramenta de pln.
           `tokens_oov_texto_mcl` - Uma lista com os tokens OOV do mcl.
           `palavra_embeddings_MEAN` - Uma lista dos embeddings de palavras com a média dos embeddings(Estratégia MEAN) dos tokens que formam a palavra.
           `palavra_embeddings_MAX` - Uma lista dos embeddings de palavras com o máximo dos embeddings(Estratégia MAX) dos tokens que formam a palavra.
        '''

        # Inicializa os dicionários de exceção
        self._inicializaDicionarioExcecao(dic_excecao_maior, dic_excecao_menor)
       
        # Constantes tokens especiais
        #SEPARADOR_TOKEN = "▁"
        #TOKEN_DESCONHECIDO = "<unk>"
       
        # Guarda os tokens e embeddings de retorno
        lista_tokens = []
        lista_tokens_oov_mcl = []
        lista_palavra_embeddings_MEAN = []
        lista_palavra_embeddings_MAX = []
        
        # Gera a tokenização e POS-Tagging da sentença    
        lista_tokens_texto_pln, lista_pos_texto_pln = pln.getListaTokensPOSTexto(tokens_texto_concatenado)

        # print("\tokens_texto_concatenado    :",tokens_texto_concatenado)    
        # print("lista_tokens_texto_pln       :",lista_tokens_texto_pln)
        # print("len(lista_tokens_texto_pln)  :",len(lista_tokens_texto_pln))    
        # print("lista_pos_texto_pln          :",lista_pos_texto_pln)
        # print("len(lista_pos_texto_pln)     :",len(lista_pos_texto_pln))
        
        # embedding <qtde_tokens x 4096>        
        # print("embeddings_texto          :",embeddings_texto.shape)
        # print("tokens_texto_mcl          :",tokens_texto_mcl)
        # print("len(tokens_texto_mcl)     :",len(tokens_texto_mcl))

        # Seleciona os pares de palavra a serem avaliadas
        pos_wi = 0 # Posição do token da palavra gerado pelo spaCy
        pos_wj = pos_wi # Posição do token da palavra gerado pelo MCL
        pos2 = -1

        # Enquanto o indíce da palavra pos_wj(2a palavra) não chegou ao final da quantidade de tokens do MCL
        while (pos_wj < len(tokens_texto_mcl)):  

            # Seleciona os tokens da sentença
            wi = lista_tokens_texto_pln[pos_wi] # Recupera o token da palavra gerado pelo spaCy
            wi1 = ""
            pos2 = -1
            if (pos_wi+1 < len(lista_tokens_texto_pln)):
                wi1 = lista_tokens_texto_pln[pos_wi+1] # Recupera o próximo token da palavra gerado pelo spaCy
      
                # Localiza o deslocamento da exceção        
                pos2 = self._getExcecaoDicMenor(wi+wi1)  
                #print("Exceção pos2:", pos2)

            wj = tokens_texto_mcl[pos_wj] # Recupera o token da palavra gerado pelo MCL
            # print("wi[",pos_wi,"]=", wi)
            # print("wj[",pos_wj,"]=", wj)

            # Tratando exceções
            # Localiza o deslocamento da exceção
            pos = self._getExcecaoDicMaior(wi)  
            #print("Exceção pos:", pos)
                
            if (pos != -1) or (pos2 != -1):      
                if pos != -1:
                    #print("Adiciona 1 Exceção palavra == wi:",wi)
                    lista_tokens.append(wi)
                    # Marca como fora do vocabulário do MCL
                    lista_tokens_oov_mcl.append(PALAVRA_FORA_DO_VOCABULARIO)
                    # Verifica se tem mais de um token
                    if (pos != 1):
                        indice_token = pos_wj + pos
                        #print("Calcula a média de :", pos_wj , "até", indice_token)
                        embeddings_tokens_palavra = embeddings_texto[pos_wj:indice_token]
                        #print("embeddings_tokens_palavra:",embeddings_tokens_palavra.shape)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular a média dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MEAN = torch.mean(embeddings_tokens_palavra, dim=0)
                        else:
                            embedding_estrategia_MEAN = np.mean(embeddings_tokens_palavra, axis=0)
                            
                        #print("embedding_estrategia_MEAN:",embedding_estrategia_MEAN.shape)
                        lista_palavra_embeddings_MEAN.append(embedding_estrategia_MEAN)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular o máximo dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MAX, linha = torch.max(embeddings_tokens_palavra, dim=0)
                        else:
                            embedding_estrategia_MAX, linha = np.max(embeddings_tokens_palavra, axis=0)
                        
                        #print("embedding_estrategia_MAX:",embedding_estrategia_MAX.shape)
                        lista_palavra_embeddings_MAX.append(embedding_estrategia_MAX)
                    else:
                        # Adiciona o embedding do token a lista de embeddings
                        lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])            
                        lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
             
                    # Avança para a próxima palavra e token do MCL
                    pos_wi = pos_wi + 1
                    pos_wj = pos_wj + pos
                    #print("Proxima:")            
                    #print("wi[",pos_wi,"]=", texto_token[pos_wi])
                    #print("wj[",pos_wj,"]=", texto_tokenizada_MCL[pos_wj])
                else:
                    if (pos2 != -1):
                        #print("Adiciona 1 Exceção palavra == wi:",wi)
                        lista_tokens.append(wi+wi1)
                        # Marca como fora do vocabulário do MCL
                        lista_tokens_oov_mcl.append(PALAVRA_FORA_DO_VOCABULARIO)
                        # Verifica se tem mais de um token
                        if (pos2 == 1): 
                            # Adiciona o embedding do token a lista de embeddings
                            lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])
                            lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
              
                        # Avança para a próxima palavra e token do MCL
                        pos_wi = pos_wi + 2
                        pos_wj = pos_wj + pos2
                        #print("Proxima:")            
                        #print("wi[",pos_wi,"]=", texto_token[pos_wi])
                        #print("wj[",pos_wj,"]=", texto_tokenizada_MCL[pos_wj])
            else:  
                # Tokens iguais adiciona a lista, o token não possui subtoken
                if (wi == wj) or (wi == wj[1:]) or (wj == self.TOKEN_DESCONHECIDO):
                    # Adiciona o token a lista de tokens
                    #print("Adiciona 2 wi==wj or wj==TOKEN_DESCONHECIDO:", wi )
                    lista_tokens.append(wi)    
                    # Marca como dentro do vocabulário do MCL
                    lista_tokens_oov_mcl.append(PALAVRA_DENTRO_DO_VOCABULARIO)
                    # Adiciona o embedding do token a lista de embeddings
                    lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])
                    lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
                    #print("embedding1[pos_wj]:", embedding_texto[pos_wj].shape)
                    # Avança para a próxima palavra e token do MCL
                    pos_wi = pos_wi + 1
                    pos_wj = pos_wj + 1   
                  
                else:          
                    # A palavra foi tokenizada pelo Wordpice com ## ou diferente do spaCy ou desconhecida
                    # Inicializa a palavra a ser montada          
                    
                    # Remove os caracteres SEPARADOR_PALAVRA("_") do token
                    if (self.SEPARADOR_TOKEN != None) and (self.SEPARADOR_TOKEN in wj):
                        palavra_POS = wj[1:]
                    else:                
                        palavra_POS = wj                    
                    
                    indice_token = pos_wj + 1                 
                    while (self.SEPARADOR_TOKEN != None) and (self.SEPARADOR_TOKEN not in tokens_texto_mcl[indice_token]) and (palavra_POS != wi) and (indice_token < len(tokens_texto_mcl)):
                       
                        # Separa o token
                        parte = tokens_texto_mcl[indice_token]
                  
                        # Concatena com a palavra
                        palavra_POS = palavra_POS + parte
                        #print("palavra_POS:",palavra_POS)
                        # Avança para o próximo token do MCL
                        indice_token = indice_token + 1

                    #print("\nMontei palavra:",palavra_POS)
                    if (palavra_POS == wi) or (palavra_POS == self.TOKEN_DESCONHECIDO):
                        # Adiciona o token a lista
                        #print("Adiciona 3 palavra == wi or palavra_POS = TOKEN_DESCONHECIDO:",wi)
                        lista_tokens.append(wi)
                        # Marca como fora do vocabulário do MCL
                        lista_tokens_oov_mcl.append(PALAVRA_FORA_DO_VOCABULARIO)
                        # Calcula a média dos tokens da palavra
                        #print("Calcula o máximo :", pos_wj , "até", indice_token)
                        embeddings_tokens_palavra = embeddings_texto[pos_wj:indice_token]
                        #print("embeddings_tokens_palavra2:",embeddings_tokens_palavra)
                        #print("embeddings_tokens_palavra2:",embeddings_tokens_palavra.shape)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular a média dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MEAN = torch.mean(embeddings_tokens_palavra, dim=0)
                            #print("embedding_estrategia_MEAN:",embedding_estrategia_MEAN)
                            #print("embedding_estrategia_MEAN.shape:",embedding_estrategia_MEAN.shape)      
                        else:
                            embedding_estrategia_MEAN = np.mean(embeddings_tokens_palavra, axis=0)      
                              
                        lista_palavra_embeddings_MEAN.append(embedding_estrategia_MEAN)
                 
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular o valor máximo dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MAX, linha = torch.max(embeddings_tokens_palavra, dim=0)
                            #print("embedding_estrategia_MAX:",embedding_estrategia_MAX)
                            #print("embedding_estrategia_MAX.shape:",embedding_estrategia_MAX.shape)     
                        else:
                             embedding_estrategia_MAX = np.max(embeddings_tokens_palavra, axis=0)
                            
                        lista_palavra_embeddings_MAX.append(embedding_estrategia_MAX)

                    # Avança para o próximo token do spaCy
                    pos_wi = pos_wi + 1
                    # Pula para o próximo token do MCL
                    pos_wj = indice_token
        
        # Verificação se as listas estão com o mesmo tamanho        
        if len(lista_tokens) !=  len(lista_tokens_texto_pln):
            logger.error("Erro na execução do método getTokensPalavrasEmbeddingsTextoSentencePiece.")
            logger.error("texto                      :{}.".format(tokens_texto_concatenado))            
            logger.error("texto_token_pln            :{}.".format(lista_tokens_texto_pln))
            logger.error("lista_pos_texto_pln        :{}.".format(lista_pos_texto_pln))
            logger.error("texto_tokenizado_mcl       :{}.".format(tokens_texto_mcl))
            logger.error("lista_tokens               :{}.".format(lista_tokens))
            logger.error("len(lista_tokens)          :{}.".format(len(lista_tokens)))
            logger.error("lista_embeddings_MEAN      :{}.".format(lista_palavra_embeddings_MEAN))
            logger.error("len(lista_embeddings_MEAN) :{}.".format(len(lista_palavra_embeddings_MEAN)))
            logger.error("lista_embeddings_MAX       :{}.".format(lista_palavra_embeddings_MAX))
            logger.error("len(lista_embeddings_MAX)  :{}.".format(len(lista_palavra_embeddings_MAX)))
       
        # Remove as variáveis que não serão mais utilizadas
        del embeddings_texto
        del tokens_texto_mcl
        del lista_tokens_texto_pln

        # Retorna os tokens de palavras e os embeddings em um dicionário
        saida = {}
        saida.update({'tokens_texto' : lista_tokens,
                      'pos_texto_pln' : lista_pos_texto_pln,
                      'tokens_oov_texto_mcl' : lista_tokens_oov_mcl,
                      'palavra_embeddings_MEAN' : lista_palavra_embeddings_MEAN,
                      'palavra_embeddings_MAX' : lista_palavra_embeddings_MAX})

        return saida
    
    # ============================  
    # getTokensPalavrasEmbeddingsTextoBPE(Roberta, GTP-2)
    # Gera os tokens, POS e embeddings de cada texto.
    def getTokensPalavrasEmbeddingsTextoBPE(self,
                                            embeddings_texto, 
                                            tokens_texto_mcl: list[str],
                                            tokens_texto_concatenado: str,
                                            pln: PLN,
                                            dic_excecao_maior:dict = {"":-1,},
                                            dic_excecao_menor:dict = {"1°":1,}) -> dict:
        '''
        De um texto preparado(tokenizado) ou não, retorna os embeddings das palavras do texto. 
        Retorna 5 listas, os tokens(palavras), as postagging, tokens OOV, e os embeddings dos tokens igualando a quantidade de tokens do spaCy com a tokenização do MCL de acordo com a estratégia. 
        Utiliza duas estratégias para realizar o pooling de tokens que forma uma palavra.
            - Estratégia MEAN para calcular a média dos embeddings dos tokens que formam uma palavra.
            - Estratégia MAX para calcular o valor máximo dos embeddings dos tokens que formam uma palavra.
            
        Parâmetros:
           `texto` - Um texto a ser recuperado os embeddings das palavras do modelo de linguagem
           `embeddings_texto` - Os embeddings do texto gerados pelo método getEmbeddingsTexto
           `tokens_texto_mcl` - Os tokens do texto gerados pelo método getEmbeddingsTexto
           `tokens_texto_concatenado` - Os tokens do texto concatenado gerados pelo método getEmbeddingsTexto
           `pln` - Uma instância da classe PLN para realizar a tokenização e POS-Tagging do texto.
           `dic_excecao_maior` - Um dicionário de tokens de exceções e seus deslocamentos para considerar mais tokens do modelo de linguagem em relação ao spaCy.
           `dic_excecao_menor` = Um dicionário de tokens de exceções e seus deslocamentos para considerar menos tokens do modelo de linguagem em relação ao spaCy.
               
        Retorna um dicionário com as seguintes chaves: 
           `tokens_texto` - Uma lista com os tokens do texto gerados pelo método.
           `pos_texto_pln` - Uma lista com as postagging dos tokens gerados pela ferramenta de pln.
           `tokens_oov_texto_mcl` - Uma lista com os tokens OOV do mcl.
           `palavra_embeddings_MEAN` - Uma lista dos embeddings de palavras com a média dos embeddings(Estratégia MEAN) dos tokens que formam a palavra.
           `palavra_embeddings_MAX` - Uma lista dos embeddings de palavras com o máximo dos embeddings(Estratégia MAX) dos tokens que formam a palavra.
        '''
 
        # Inicializa os dicionários de exceção
        self._inicializaDicionarioExcecao(dic_excecao_maior, dic_excecao_menor)
       
        # Constantes tokens especiais
        #SEPARADOR_TOKEN = "Ġ"
        #TOKEN_DESCONHECIDO = "Â"
       
        # Guarda os tokens e embeddings de retorno
        lista_tokens = []
        lista_tokens_oov_mcl = []
        lista_palavra_embeddings_MEAN = []
        lista_palavra_embeddings_MAX = []
        
        # Gera a tokenização e POS-Tagging da sentença    
        lista_tokens_texto_pln, lista_pos_texto_pln = pln.getListaTokensPOSTexto(tokens_texto_concatenado)

        # print("\tokens_texto_concatenado    :",tokens_texto_concatenado)    
        # print("lista_tokens_texto_pln       :",lista_tokens_texto_pln)
        # print("len(lista_tokens_texto_pln)  :",len(lista_tokens_texto_pln))    
        # print("lista_pos_texto_pln          :",lista_pos_texto_pln)
        # print("len(lista_pos_texto_pln)     :",len(lista_pos_texto_pln))
        
        # embedding <qtde_tokens x 4096>        
        # print("embeddings_texto          :",embeddings_texto.shape)
        # print("tokens_texto_mcl          :",tokens_texto_mcl)
        # print("len(tokens_texto_mcl)     :",len(tokens_texto_mcl))

        # Seleciona os pares de palavra a serem avaliadas
        pos_wi = 0 # Posição do token da palavra gerado pelo spaCy
        pos_wj = pos_wi # Posição do token da palavra gerado pelo MCL
        pos2 = -1

        # Enquanto o indíce da palavra pos_wj(2a palavra) não chegou ao final da quantidade de tokens do MCL
        while (pos_wj < len(tokens_texto_mcl)):  

            # Seleciona os tokens da sentença
            wi = lista_tokens_texto_pln[pos_wi] # Recupera o token da palavra gerado pelo spaCy
            wi1 = ""
            pos2 = -1
            if (pos_wi+1 < len(lista_tokens_texto_pln)):
                wi1 = lista_tokens_texto_pln[pos_wi+1] # Recupera o próximo token da palavra gerado pelo spaCy
      
                # Localiza o deslocamento da exceção        
                pos2 = self._getExcecaoDicMenor(wi+wi1)  
                #print("Exceção pos2:", pos2)

            wj = tokens_texto_mcl[pos_wj] # Recupera o token da palavra gerado pelo MCL
            # print("wi[",pos_wi,"]=", wi)
            # print("wj[",pos_wj,"]=", wj)

            # Tratando exceções
            # Localiza o deslocamento da exceção
            pos = self._getExcecaoDicMaior(wi)  
            #print("Exceção pos:", pos)
                
            if (pos != -1) or (pos2 != -1):      
                if pos != -1:
                    #print("Adiciona 1 Exceção palavra == wi:",wi)
                    lista_tokens.append(wi)
                    # Marca como fora do vocabulário do MCL
                    lista_tokens_oov_mcl.append(PALAVRA_FORA_DO_VOCABULARIO)
                    # Verifica se tem mais de um token
                    if (pos != 1):
                        indice_token = pos_wj + pos
                        #print("Calcula a média de :", pos_wj , "até", indice_token)
                        embeddings_tokens_palavra = embeddings_texto[pos_wj:indice_token]
                        #print("embeddings_tokens_palavra:",embeddings_tokens_palavra.shape)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular a média dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MEAN = torch.mean(embeddings_tokens_palavra, dim=0)
                        else:
                            embedding_estrategia_MEAN = np.mean(embeddings_tokens_palavra, axis=0)
                            
                        #print("embedding_estrategia_MEAN:",embedding_estrategia_MEAN.shape)
                        lista_palavra_embeddings_MEAN.append(embedding_estrategia_MEAN)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular o máximo dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MAX, linha = torch.max(embeddings_tokens_palavra, dim=0)
                        else:
                            embedding_estrategia_MAX, linha = np.max(embeddings_tokens_palavra, axis=0)
                        
                        #print("embedding_estrategia_MAX:",embedding_estrategia_MAX.shape)
                        lista_palavra_embeddings_MAX.append(embedding_estrategia_MAX)
                    else:
                        # Adiciona o embedding do token a lista de embeddings
                        lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])            
                        lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
             
                    # Avança para a próxima palavra e token do MCL
                    pos_wi = pos_wi + 1
                    pos_wj = pos_wj + pos
                    #print("Proxima:")            
                    #print("wi[",pos_wi,"]=", texto_token[pos_wi])
                    #print("wj[",pos_wj,"]=", texto_tokenizada_MCL[pos_wj])
                else:
                    if (pos2 != -1):
                        #print("Adiciona 1 Exceção palavra == wi:",wi)
                        lista_tokens.append(wi+wi1)
                        # Marca como fora do vocabulário do MCL
                        lista_tokens_oov_mcl.append(self.PALAVRA_FORA_DO_VOCABULARIO)
                        # Verifica se tem mais de um token
                        if (pos2 == 1): 
                            # Adiciona o embedding do token a lista de embeddings
                            lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])
                            lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
              
                        # Avança para a próxima palavra e token do MCL
                        pos_wi = pos_wi + 2
                        pos_wj = pos_wj + pos2
                        #print("Proxima:")            
                        #print("wi[",pos_wi,"]=", texto_token[pos_wi])
                        #print("wj[",pos_wj,"]=", texto_tokenizada_MCL[pos_wj])
            else:  
                # Tokens iguais adiciona a lista, o token não possui subtoken
                if (wi == wj) or (wi == wj[1:]) or (wj[0] == self.TOKEN_DESCONHECIDO):
                    # Adiciona o token a lista de tokens
                    #print("Adiciona 2 wi==wj or wj==TOKEN_DESCONHECIDO[0]:", wi )
                    lista_tokens.append(wi)    
                    # Marca como dentro do vocabulário do MCL
                    lista_tokens_oov_mcl.append(PALAVRA_DENTRO_DO_VOCABULARIO)
                    # Adiciona o embedding do token a lista de embeddings
                    lista_palavra_embeddings_MEAN.append(embeddings_texto[pos_wj])
                    lista_palavra_embeddings_MAX.append(embeddings_texto[pos_wj])
                    #print("embedding1[pos_wj]:", embedding_texto[pos_wj].shape)
                    # Avança para a próxima palavra e token do MCL
                    pos_wi = pos_wi + 1
                    pos_wj = pos_wj + 1   
                  
                else:          
                    # A palavra foi tokenizada pelo Wordpice com ## ou diferente do spaCy ou desconhecida
                    # Inicializa a palavra a ser montada          
                    
                    # Remove os caracteres SEPARADOR_PALAVRA("_") do token
                    if (self.SEPARADOR_TOKEN != None) and (self.SEPARADOR_TOKEN in wj):
                        palavra_POS = wj[1:]
                    else:                
                        palavra_POS = wj                    
                    
                    indice_token = pos_wj + 1                 
                    while (self.SEPARADOR_TOKEN != None) and (self.SEPARADOR_TOKEN not in tokens_texto_mcl[indice_token]) and (palavra_POS != wi) and (indice_token < len(tokens_texto_mcl)):
                       
                        # Separa o token
                        if (self.SEPARADOR_TOKEN != None) and (self.SEPARADOR_TOKEN in tokens_texto_mcl[indice_token]):
                            # Remove os caracteres SEPARADOR_TOKEN("G") do token
                            parte = tokens_texto_mcl[indice_token][1:]                            
                        else:
                            parte = tokens_texto_mcl[indice_token]                            
                  
                        # Concatena com a palavra
                        palavra_POS = palavra_POS + parte
                        #print("palavra_POS:",palavra_POS)
                        # Avança para o próximo token do MCL
                        indice_token = indice_token + 1

                    #print("\nMontei palavra:",palavra_POS)
                    if (palavra_POS == wi) or (palavra_POS[0] == self.TOKEN_DESCONHECIDO):
                        # Adiciona o token a lista
                        #print("Adiciona 3 palavra == wi or palavra_POS = TOKEN_DESCONHECIDO:",wi)
                        lista_tokens.append(wi)
                        # Marca como fora do vocabulário do MCL
                        lista_tokens_oov_mcl.append(PALAVRA_FORA_DO_VOCABULARIO)
                        # Calcula a média dos tokens da palavra
                        #print("Calcula o máximo :", pos_wj , "até", indice_token)
                        embeddings_tokens_palavra = embeddings_texto[pos_wj:indice_token]
                        #print("embeddings_tokens_palavra2:",embeddings_tokens_palavra)
                        #print("embeddings_tokens_palavra2:",embeddings_tokens_palavra.shape)
                        
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular a média dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MEAN = torch.mean(embeddings_tokens_palavra, dim=0)
                            #print("embedding_estrategia_MEAN:",embedding_estrategia_MEAN)
                            #print("embedding_estrategia_MEAN.shape:",embedding_estrategia_MEAN.shape)      
                        else:
                            embedding_estrategia_MEAN = np.mean(embeddings_tokens_palavra, axis=0)      
                              
                        lista_palavra_embeddings_MEAN.append(embedding_estrategia_MEAN)
                 
                        if isinstance(embeddings_tokens_palavra, torch.Tensor): 
                            # calcular o valor máximo dos embeddings dos tokens do MCL da palavra
                            embedding_estrategia_MAX, linha = torch.max(embeddings_tokens_palavra, dim=0)
                            #print("embedding_estrategia_MAX:",embedding_estrategia_MAX)
                            #print("embedding_estrategia_MAX.shape:",embedding_estrategia_MAX.shape)     
                        else:
                             embedding_estrategia_MAX = np.max(embeddings_tokens_palavra, axis=0)
                            
                        lista_palavra_embeddings_MAX.append(embedding_estrategia_MAX)

                    # Avança para o próximo token do spaCy
                    pos_wi = pos_wi + 1
                    # Pula para o próximo token do MCL
                    pos_wj = indice_token
        
        # Verificação se as listas estão com o mesmo tamanho        
        if len(lista_tokens) !=  len(lista_tokens_texto_pln):
            logger.error("Erro na execução do método getTokensPalavrasEmbeddingsTextoBPE.")
            logger.error("texto                      :{}.".format(tokens_texto_concatenado))            
            logger.error("texto_token_pln            :{}.".format(lista_tokens_texto_pln))
            logger.error("lista_pos_texto_pln        :{}.".format(lista_pos_texto_pln))
            logger.error("texto_tokenizado_mcl       :{}.".format(tokens_texto_mcl))
            logger.error("lista_tokens               :{}.".format(lista_tokens))
            logger.error("len(lista_tokens)          :{}.".format(len(lista_tokens)))
            logger.error("lista_embeddings_MEAN      :{}.".format(lista_palavra_embeddings_MEAN))
            logger.error("len(lista_embeddings_MEAN) :{}.".format(len(lista_palavra_embeddings_MEAN)))
            logger.error("lista_embeddings_MAX       :{}.".format(lista_palavra_embeddings_MAX))
            logger.error("len(lista_embeddings_MAX)  :{}.".format(len(lista_palavra_embeddings_MAX)))
       
        # Remove as variáveis que não serão mais utilizadas
        del embeddings_texto
        del tokens_texto_mcl
        del lista_tokens_texto_pln

        # Retorna os tokens de palavras e os embeddings em um dicionário
        saida = {}
        saida.update({'tokens_texto' : lista_tokens,
                      'pos_texto_pln' : lista_pos_texto_pln,
                      'tokens_oov_texto_mcl' : lista_tokens_oov_mcl,
                      'palavra_embeddings_MEAN' : lista_palavra_embeddings_MEAN,
                      'palavra_embeddings_MAX' : lista_palavra_embeddings_MAX})

        return saida
    
    # ============================   
    def getDimensaoEmbedding(self) -> int:
        '''
        Retorna a dimensão do embedding
        '''

        return self.auto_model.config.hidden_size        
        
    # ============================   
    def save(self, output_path: str):
        '''
        Salva o modelo.

        Parâmetros:
           `output_path` - caminho para salvar o modelo
        '''

        self.auto_model.save_pretrained(output_path)
        self.auto_tokenizer.save_pretrained(output_path)

        with open(os.path.join(output_path, 'modelo_linguagem_config.json'), 'w') as fOut:
            json.dump(self.get_config_dict(), fOut, indent=2)

    # ============================   
    def getAutoModel(self):
        '''
        Recupera o modelo.
        '''

        return self.auto_model

    # ============================   
    def getAutoTokenizer(self):
        '''
        Recupera o tokenizador.
        '''

        return self.auto_tokenizer

    # ============================   
    def batchToDevice(self, lote, 
                      target_device: device):
        '''
        Envia lote pytorch batch para um dispositivo (CPU/GPU)

        Parâmetros:
           `lote` - lote pytorch
           `target_device` - dispositivo de destino (CPU/GPU)
        
        Retorno:
           lote enviado para o dispositivo        
        '''

        for key in lote:
            if isinstance(lote[key], Tensor):
                lote[key] = lote[key].to(target_device)
                
        return lote
    
    # ============================   
    def trataListaTokensEspeciais(self, tokens_texto_mcl):    
        '''
        Trata a lista de tokens tokenizador do MCL.

        Parâmetros:
           `tokens_texto_mcl` - Lista dos tokens gerados pelo tokenizador.
           
        Retorno:
           Lista de tokens tratada.        
        '''  
        
        # Se o primeiro token não for o TOKEN_INICIO e o token tem caracter inicial igual ao separador, remove
        if (self.TOKEN_INICIO != None) and (self.TOKEN_INICIO != tokens_texto_mcl[0]) and (self.SEPARADOR_TOKEN != tokens_texto_mcl[0][0]):
        
            tokens_texto_mcl = [self.SEPARADOR_TOKEN + tokens_texto_mcl[0]] + tokens_texto_mcl[1:]
            #print("tokens_texto_mcl:", tokens_texto_mcl)
        
        return tokens_texto_mcl
