import numpy as np
import warnings
from sklearn.exceptions import UndefinedMetricWarning
class Resultado():
    def __init__(self, y, predict_y):
        """
        y: Vetor numpy (np.array) em que, para cada instancia i, y[i] é a classe alvo da mesma
        predict_y: Vetor numpy (np.array) que cada elemento y[i] representa a predição da instancia i

        Tanto y quando predict_y devem assumir valores numéricos
        """
        self.y = y
        self.predict_y = predict_y
        self._mat_confusao = None
        self._precisao = None
        self._revocacao = None

    @property
    def mat_confusao(self):
        """
        Retorna a matriz de confusão.
        """
        #caso a matriz de confusao já esteja calculada, retorna-la
        if self._mat_confusao is not None:
            return self._mat_confusao

        #instancia a matriz de confusao como uma matriz de zeros
        #A matriz de confusão terá o tamanho como o máximo entre os valores de self.y e self.predict_y
        max_class_val = max([self.y.max(),self.predict_y.max()])
        self._mat_confusao = np.zeros((max_class_val+1,max_class_val+1))
        
        #incrementa os valores da matriz baseada nas listas self.y e self.predict_y
        for i,classe_real in enumerate(self.y):
            self._mat_confusao[classe_real][self.predict_y[i]] += 1

        #print("Predict y: "+str(self.predict_y))
        #print("y: "+str(self.y))
        #print("Matriz de confusao final :"+str(self._mat_confusao))
        return self._mat_confusao


    @property
    def acuracia(self):
        #quantidade de elementos previstos corretamente
        num_previstos_corretamente = 0
        total_previstos = 0
        for classe in range(len(self.mat_confusao)):
            #substitua o "None" para que seja calculado o numero de elementos previstos corretamente
            num_previstos_corretamente += self._mat_confusao[classe][classe]
            total_previstos += sum(self._mat_confusao[classe])
        #substitua o None para que seja calculado a acurácia
        return num_previstos_corretamente/total_previstos

    @property
    def precisao(self):
        """
        Precisão por classe
        """
        if self._precisao is not None:
            return self._precisao

        #inicialize com um vetor de zero usando np.zeros
        self._precisao = np.zeros(len(self.mat_confusao))

        #para cada classe, armazene em self._precisao[classe] o valor relativo à precisão
        #dessa classe
        for classe in range(len(self.mat_confusao)):
            #Abaixo, navegue em self.mat_confusao para efetuar o calculo da precisão
            soma = 0
            #você pode mudar o nome "classe_b" para um nome melhor (classe_real ou classe_prevista?)
            for classe_b in range(len(self.mat_confusao)):
                soma += self.mat_confusao[classe_b][classe]

            #armazene no veotr a precisão para a classe, não deixe que ocorra divisão por zero
            #caso ocorra, faça um warning
            if soma != 0: #altere o "None" para que nao ocorra divisão por zero
                self._precisao[classe] =  self.mat_confusao[classe][classe] / soma #altere o "None" para o código correto
            else:
                self._precisao[classe] = 0
                ##complete aqui com a foroma de assinatura correta da função warn -
                ## Deverá ser lançada uma UndefinedMetricWarning
                warnings.warn("divisão por zero no cálculo da precisão", UndefinedMetricWarning)
        return self._precisao
    @property
    def revocacao(self):
        if self._revocacao is not None:
            return self._revocacao

        self._revocacao = np.zeros(len(self.mat_confusao))
        for classe in range(len(self.mat_confusao)):
            #Abaixo, navegue em self.mat_confusao para efetuar o calculo da precisão
            soma = 0
            #você pode mudar o nome "classe_b" para um nome melhor (classe_real ou classe_prevista?)
            for classe_b in range(len(self.mat_confusao)):
                soma += self.mat_confusao[classe][classe_b] #altere o "None" para o código correto

            #armazene no veotr a precisão para a classe, não deixe que ocorra divisão por zero
            #caso ocorra, faça um warning
            if soma != 0:#altere o "None" para que nao ocorra divisão por zero
                self._revocacao[classe] =  self.mat_confusao[classe][classe] / soma #altere o "None" para o código correto
            else:
                self._revocacao[classe] = 0
                ##complete aqui com a foroma de assinatura correta da função warn -
                ## Deverá ser lançada uma UndefinedMetricWarning
                warnings.warn("divisão por zero no cálculo da revocação", UndefinedMetricWarning)
        return self._revocacao

    @property
    def f1_por_classe(self):
        """
        retorna um vetor em que, para cada classe, retorna o seu f1
        """

        #f1 é o veor de f1 que deve ser retornado. Altere o "None" com o tamanho correto do vetor
        f1 = np.zeros(len(self.mat_confusao))

        for classe in range(len(self.mat_confusao)):
            #faça o calculo do f1. Assegure-se que não haja divisão por zero.
            #substitua os "None" para que o código abaixo funcione
            dem = (self.precisao[classe]+self.revocacao[classe])
            if(dem != 0):
                f1[classe] = (2*self.precisao[classe]*self.revocacao[classe])/dem
            else:
                f1[classe] = -1
        return f1

    @property
    def macro_f1(self):
        """
        Calcula o macro f1
        """
        positives = self.f1_por_classe > 0
        print("positives")
        print(positives)
        if positives.any():
            return self.f1_por_classe[positives].mean()
        else:
            return 0.
        #return np.average(self.f1_por_classe)

class Fold():
    def __init__(self,df_treino,df_data_to_predict,col_classe):
        self.df_treino = df_treino
        self.df_data_to_predict = df_data_to_predict
        self.col_classe = col_classe


    def eval(self,ml_method):
        #a partir de self.df_treino, separe as features (em x_treino) da classe (em y_treino)
        x_treino = self.df_treino.drop([self.col_classe], axis=1)
        y_treino = self.df_treino[self.col_classe]

        #use o método fit do scikit learn para criar o modelo usando x_treino e y_treino
        model = ml_method.fit(x_treino, y_treino)

        #De forma similar ao que foi feito em self.df_treino,
        #a partir de self.df_data_to_predict, separe as features e as classes a serem previstas
        x_to_predict = self.df_data_to_predict.drop([self.col_classe], axis=1)
        y_to_predict = self.df_data_to_predict[self.col_classe]

        #realize as predicoes usando o método predict do scikit learn
        y_predictions = model.predict(x_to_predict)

        #Impressao do x e y
        # print("X_treino: "+str(x_treino))
        # print("y_treino: "+str(y_treino))
        # print("X_to_predict: "+str(x_to_predict))
        # print("y_to_predict: "+str(y_to_predict))
        # print("y_predictions: "+str(y_predictions))

        #retorne o resultado
        return Resultado(y_to_predict,y_predictions)
