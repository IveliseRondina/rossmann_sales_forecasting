import os
import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann
# from  pasta.arquivo.py import class

# loading model
model = pickle.load( open('model/model_rossmann.pkl', 'rb' ) )

# initialize API
app = Flask( __name__ ) # instanciar classe ler sobre # instancia e criar uma copia da classe

@app.route( '/rossmann/predict', methods=['POST'] ) #ENDPOINT # POST precisa receber dado p/ retornar, GET retorna sem receber
def rossmann_predict(): # toda vez que o endpoint post recebe ele executa a funcao abaixo dele
    test_json = request.get_json() # pega os dados que sao enviados via API
    
    if test_json:  # there is data
        if isinstance( test_json, dict ): # Unique Example ### verificando se veio 1 ou mais datasets
            test_raw = pd.DataFrame( test_json, index=[0] ) # para jsons de uma unica linha
        
        else: # Multiple examples
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() ) # pega as keys do dicionarios(json) e usa como title das colunas
        
        # Instantiate Rossmann class
        pipeline = Rossmann()
        
        # data cleaning
        df1 = pipeline.data_cleaning( test_raw ) #  como se fosse uma funcao ex pd.read(), o pipeline e o apelido do rossmann
        
        # feature engineering
        df2 = pipeline.feature_engineering( df1 )
        
        # data preparation
        df3 = pipeline.data_preparation( df2 )
        
        # prediction
        df_response = pipeline.get_prediction( model, test_raw, df3 ) # retorna modelo, dados originais, e predicao
        
        return df_response
        
        
        
    else:
        return Response( '{}', status=200, mimetype='application/json' ) # status200 significa que o request funcionou mas veio vazio


if __name__ == '__main__':
    port = os.environ.get( 'PORT', 5000 )
    app.run( host='0.0.0.0', port=port )
