from math import sqrt
from matplotlib.pyplot import plot, title, show, annotate
import matplotlib.pyplot as plt
from random import random, randrange, choice, uniform, randint, sample
import pprint
pp = pprint.PrettyPrinter()

class Individuo():

    def __init__(self, tamanhoCromo, geracao = 0):
        self.cromossomo = []
        self.tamanhoCromo = tamanhoCromo
        self.geracao = geracao
        self.fitness = 0
        self.limites = [5.12,-5.12]
        self.gerarCromossomo()
        self.calculaFitness()


    def gerarCromossomo(self):
        cromo = []
        for i in range(self.tamanhoCromo):
            cromo.append(uniform(self.limites[0], self.limites[1]))
        self.cromossomo = cromo

    def dejong(self, dimensoes):
        return sum(dimensoes[x]**2 for x in range(len(dimensoes)))


    def calculaFitness(self):
        dejongvalue = self.dejong(self.cromossomo)
        self.fitness = 1 / (dejongvalue + 1)
        
        return self.fitness

    def __repr__(self):
        return 'Geração %s Fitness %s ' % (self.geracao, str(self.fitness))


class DE():

    def __init__(self, limites, tamanhoPopulacao, tamanhoCromossomo, interacoes, fatorCrossover, fatorMutacao):
        self.tamanhoPopulacao = tamanhoPopulacao
        self.tamanhoCromossomo = tamanhoCromossomo
        self.interacoes = interacoes
        self.fatorCrossover = fatorCrossover
        self.fatorMutacao = fatorMutacao
        self.populacao = []
        self.historicoFitness = []
        self.melhor = None
        self.limites = limites
        self.historicoMedia = []
        self.somaMedia = 0.0

    def setMelhor(self, individuo):
        if self.melhor == None:
            self.melhor = individuo
        elif self.melhor.fitness > individuo.fitness:
            self.melhor = individuo
        
    def gerarPopulacao(self):
        for i in range(self.tamanhoPopulacao):
            ind = Individuo(self.tamanhoCromossomo)
            ind.gerarCromossomo()
            ind.calculaFitness()
            self.populacao.append(ind)

    def selecao(self, naoEscolher):
        ''' Selecionado 3 individuos alfa, beta e gama. Exceto o que será o 
            alvo, no caso representado pela variável naoEscolher'''       
        indice = [x for x in range(len(self.populacao))]
        indice.remove(naoEscolher)                
        
        sel = sample(indice, 3)
        r = []
        r.append(self.populacao[sel[0]])
        r.append(self.populacao[sel[1]])
        r.append(self.populacao[sel[2]])
        return r

    def vertorModificado(self, individuos):
        alfa = individuos[0]
        beta = individuos[1]
        gama = individuos[2]

        tamanhoCromo = len(alfa.cromossomo)
        vetorExperimental = []
        for i in range(tamanhoCromo):
            mut = alfa.cromossomo[i] + self.fatorMutacao * (beta.cromossomo[i] - gama.cromossomo[i])                                
            vetorExperimental.append(mut)

        ind = Individuo(self.tamanhoCromossomo)
        ind.cromossomo = vetorExperimental
        ind.calculaFitness()
        return ind

    
    def crossoverBi(self, alvo, individuoModificado):
        vetorExperimental = []
        for i in range(individuoModificado.tamanhoCromo):
            '''Crossover Binomial, gera um valor randômico "a" e se for maior 
               que o fator crossover pega do modificado(mutação)'''
            a = random()
            if a <= self.fatorCrossover:
                vetorExperimental.append(individuoModificado.cromossomo[i])
            else:
                vetorExperimental.append(alvo.cromossomo[i])

        ind = Individuo(self.tamanhoCromossomo)
        ind.cromossomo = vetorExperimental
        ind.calculaFitness()
        return ind

    def torneio(self, individuoExperimental, corrente):
        if individuoExperimental.fitness < corrente.fitness:            
            self.historicoFitness.append(individuoExperimental.fitness)
            self.setMelhor(individuoExperimental)
            self.setHistoricoMedia(individuoExperimental)
            return individuoExperimental                        
        else:
            self.historicoFitness.append(corrente.fitness)
            self.setHistoricoMedia(corrente)
            return corrente

    def setHistoricoMedia(self, solucao):
        if self.somaMedia == 0:
            self.somaMedia = solucao.fitness
            self.historicoMedia.append(solucao.fitness)
        else:
            self.somaMedia = self.somaMedia + solucao.fitness        
            self.historicoMedia.append(self.somaMedia / (len(self.historicoMedia)+1))
        

    def run(self):
        self.gerarPopulacao()

        for i in range(self.interacoes):
            individuoModificado = None
            newPopulacao = []
            for p in range(len(self.populacao)):
                ''' Selecionado 3 individuos alfa, beta e gama. Exceto o alvo, no caso representado pela variável p'''       
                selecao = self.selecao(p)                
                
                '''Gerando o vetor modificado'''    
                individuoModificado = self.vertorModificado(selecao)
                
                '''Gerando o experimental com cruzamento binomial'''
                individuoExperimental = self.crossoverBi(self.populacao[p], individuoModificado)
                
                '''Torneio para saver se o experimental é melhor que o vetor alvo '''
                newInd = self.torneio(individuoExperimental, self.populacao[p])
                newInd.geracao = i
                
                '''Adicionado para proxima população o novo vetor que ganho no torneio '''
                newPopulacao.append(newInd)
                
            self.populacao = newPopulacao

        print('O Individuo que teve melhor desempenho %s' % self.melhor)
        
        
        self.historicoFitness.sort(reverse=True)
        self.historicoMedia.sort(reverse=True)        
        plt.plot(self.historicoFitness, 'r', label='Melhor')        
        plt.plot(self.historicoMedia, 'g', label='Média')        
        plt.legend()
        plt.title("Convegência das gerações RAND/1/BIN")
        
        plt.xlabel('Geração')
        plt.ylabel('Valor da função de avaliação ')
        plt.show()        
        


if __name__ == '__main__':

    limites = [5.12, -5.12]
    tamanhoPopulacao = 10
    tamanhoCromossomo = 20
    interacoes = 200
    fatorCrossover = 0.9
    fatorMutacao = 0.6

    de = DE(limites, tamanhoPopulacao, tamanhoCromossomo, interacoes, fatorCrossover, fatorMutacao)
    de.run()


