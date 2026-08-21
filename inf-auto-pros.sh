#!/bin/bash

ARQUIVO_CSV="sp_234_l1_transc_cer_wer.csv"
PASTA_ORIGEM="SP_DID_234"
PASTA_DESTINO="output/final"
PASTA_TMP_RESULT="output/result/cmltts_entoa_pros"
PASTA_TMP_RESULT_AUTO="output/result/cmltts_entoa_auto"

# Cria as pastas necessárias caso não existam
mkdir -p "$PASTA_DESTINO"
mkdir -p "$PASTA_TMP_RESULT"
mkdir -p "$PASTA_TMP_RESULT_AUTO"

if [ ! -f "$ARQUIVO_CSV" ]; then
    echo "Erro: O arquivo '$ARQUIVO_CSV' não foi encontrado."
    exit 1
fi

echo "Iniciando o processamento..."

awk -v FPAT='([^,]*)|(\"[^\"]*\")' 'NR > 1 {
    # Remove as aspas do início e do fim
    gsub(/^"|"$/, "", $1)
    gsub(/^"|"$/, "", $2)
    
    # Imprime a coluna 1 e 2 separadas por um TAB
    print $1 "\t" $2
}' "$ARQUIVO_CSV" | while IFS=$'\t' read -r path human; do
    
    ARQUIVO_AUDIO="$PASTA_ORIGEM/$path"
    
    if [ -f "$ARQUIVO_AUDIO" ]; then
        echo "---------------------------------------------------"
        echo "Processando: $path"
        
        # Comando 1: Copiar o arquivo original
        cp "$ARQUIVO_AUDIO" "$PASTA_DESTINO/"
        
        # Limpa arquivos .wav residuais da pasta de resultado antes de gerar um novo.
        # Isso garante que só vamos mover o áudio gerado AGORA.
        rm -f "$PASTA_TMP_RESULT"/*.wav
        
        # Comando 2: Gerar o áudio usando o texto da coluna 'human'
        echo "Sintetizando áudio para o texto..."
        python synthesize.py --text "$human" \
         --speaker_id 54 --restore_step 720000 --mode single \
         -p config/cmltts_entoa_pros/preprocess.yaml \
         -m config/cmltts_entoa_pros/model.yaml \
         -t config/cmltts_entoa_pros/train.yaml
        
        # Comando 3: Criar o novo nome e mover o arquivo
        # Pega o nome original, retira o ".wav" e adiciona "_pros.wav"
        NOVO_NOME="${path%.wav}_pros.wav"
        
        # Verifica se o script python realmente gerou um .wav na pasta
        if ls "$PASTA_TMP_RESULT"/*.wav 1> /dev/null 2>&1; then
            # Move o .wav gerado para a pasta final já com o novo nome
            mv "$PASTA_TMP_RESULT"/*.wav "$PASTA_DESTINO/$NOVO_NOME"
            echo "Áudio gerado movido para: $PASTA_DESTINO/$NOVO_NOME"
        else
            echo "Erro: O script python não gerou nenhum arquivo .wav para $path"
        fi


        rm -f "$PASTA_TMP_RESULT_AUTO"/*.wav
        
        echo "Sintetizando áudio para o texto..."
        python synthesize.py --text "$human" \
         --speaker_id 93 --restore_step 720000 --mode single \
         -p config/cmltts_entoa_auto/preprocess.yaml \
         -m config/cmltts_entoa_auto/model.yaml \
         -t config/cmltts_entoa_auto/train.yaml
        
        NOVO_NOME="${path%.wav}_auto.wav"
        
        # Verifica se o script python realmente gerou um .wav na pasta
        if ls "$PASTA_TMP_RESULT_AUTO"/*.wav 1> /dev/null 2>&1; then
            # Move o .wav gerado para a pasta final já com o novo nomels -
            mv "$PASTA_TMP_RESULT_AUTO"/*.wav "$PASTA_DESTINO/$NOVO_NOME"
            echo "Áudio gerado movido para: $PASTA_DESTINO/$NOVO_NOME"
        else
            echo "Erro: O script python não gerou nenhum arquivo .wav para $path"
        fi


    else
        echo "Aviso: Arquivo original '$ARQUIVO_AUDIO' não encontrado! Pulando..."
    fi
    
done

echo "---------------------------------------------------"
echo "Processamento concluído com sucesso!"