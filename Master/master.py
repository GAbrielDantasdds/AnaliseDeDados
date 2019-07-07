import matplotlib.pyplot as plt
from operator import itemgetter


class Arquivo():
    def __init__(self, nome = 'XYZ999.txt'):
        self.arquivo = open(nome, 'r')
        self.dados = []
        
    def quebrar_linhas(self):
        for linha in self.arquivo:
            linha = linha.strip()
            linha = linha.split(',')
            self.dados.append(linha)
        return self.dados
            
    def media_grau(self):
        
        notas = []
        dados = Arquivo().quebrar_linhas()
        
        for linha in dados:
            if '.' in linha[3]:
                notas.append(float(linha[3]))
                
        total = sum(notas)
        md = len(notas)
        media = total/md
        print('Média geral da disciplina considerando todos os anos e cursos: {}'
              .format(round(media, 2)))

    def grau_por_curso(self):
        
        dados = Arquivo().quebrar_linhas()
        
        cursos = {
            'Engenharia Civil': [],
            'Engenharia de Produção': [],
            'Engenharia Mecânica': []
            }

        for linha in dados:
            cursos[linha[1]] = cursos[linha[1]] + [float(linha[3])]
        for curso in cursos:
            soma = sum(cursos[curso])
            md = len(cursos[curso])
            media = soma/md
            print('{} tem média de grau igual a: {:2}'
                  .format(curso, round(media, 2)))
            

    def maior_grau_p(self):

        dados = Arquivo().quebrar_linhas()

        peri = []
        med = []
        periodos = {}
        medias = {}

        for linha in dados:
            periodos[linha[2]] = []
        for linha in dados:
            periodos[linha[2]] = periodos[linha[2]] + [float(linha[3])]

        for p in periodos:
            soma = sum(periodos[p])
            md = len(periodos[p])
            media = soma/md
            medias[p] = round(media, 2)

        for chave, valor in medias.items():
            peri.append(chave)
            med.append(valor)

        maior = peri[med.index(max(med))]
        menor = peri[med.index(min(med))]
        
        print('Período com maior média de grau: {}'.format(maior))
        print('Período com menor média de grau: {}'.format(menor))

    def reprovados(self):

        dados = Arquivo().quebrar_linhas()

        reprovados = 0
        matri = []
        
        for linha in dados:
            if linha[0] not in matri:
                matri.append(linha[0])
            if float(linha[3]) < 5.0:
                reprovados += 1
        
        perc  = (reprovados*100)/len(matri)
        print('Percentual de alunos que reprovaram foi de: {}%'.format(perc))

    def matriculas():

        dados = Arquivo().quebrar_linhas()

        
        matriculas = []
        matricula = {}

        for linha in dados:
            if linha[0] not in matriculas:
                matriculas.append(linha[0])
            else:
                matricula[linha[0]] = [0]

        for linha in dados:
            try:
                if matricula[linha[0]]:
                    matricula[linha[0]].extend([float(linha[2]), float(linha[3])])
            except:
                pass
            
        return matricula

    def desistentes(self):

        dic = Arquivo.matriculas()


        desistiu = 0

        for ii in dic:
            periodo_maior_esq = dic[ii][1] > dic[ii][3]
            grau_maior_esq = dic[ii][2]  > dic[ii][4]

            periodo_maior_dir = dic[ii][1] < dic[ii][3]
            grau_maior_dir = dic[ii][2]  < dic[ii][4]

            if periodo_maior_esq:
                if grau_maior_esq:
                    pass
                else:
                    desistiu +=1
            if periodo_maior_dir:
                if grau_maior_dir:
                    pass
                else:
                    
                    desistiu +=1
            
        
        print('Alunos desistentes: {}'.format(desistiu))

    def grf_md_curso(self):

        dados = Arquivo().quebrar_linhas()
        

        cursos = {
            'Engenharia Civil': [],
            'Engenharia de Produção': [],
            'Engenharia Mecânica': []
            }

        for linha in dados:
            cursos[linha[1]] = cursos[linha[1]] + [float(linha[3])]
        for curso in cursos:
            soma = sum(cursos[curso])
            md = len(cursos[curso])
            media = soma/md
            cursos[curso] = round(media,2)
            
        plt.plot(['Engenharia Civil', 'Engenharia de Produção','Engenharia Mecânica'], [item for item in cursos.values()])
        plt.ylabel('Médias')
        plt.title('Grau médio por período')
        plt.ylim(6.90,7.20)
        plt.savefig('media_curso.png')

    def grf_md_pe(self):
        
        dados = Arquivo().quebrar_linhas()
        

        peri = {}

        for linha in dados:
            peri[linha[2]] = []
        for ii in dados:
            peri[ii[2]].extend([float(ii[3])])
            
        for nota in peri:
            soma = sum(peri[nota])
            md = len(peri[nota])
            media = soma/md
            peri[nota] = round(media, 2)


        peri = sorted(peri.items(), key=itemgetter(0))

        perii = {}

        
        for item in peri:
            perii[item[0]] = item[1]

        plt.figure(figsize=(8,5))
        
        z  = []
        w = []
        l = []
        for x,y in perii.items():
            plt.bar(x,y)
            #z.append(y)
            w.append(x)
        for i in range(len(w)):
            l.append(i)
        plt.xticks(l, w, rotation='vertical')
        plt.subplots_adjust(bottom=0.20)
        #plt.margins(0.2)
        plt.title('Gráfico por período')
        plt.ylabel('Grau')
        plt.xlabel('Períodos')
        plt.ylim(6.4,7.5)
        plt.savefig('media_curso_periodo.png')
            
    def grf_reprova_curso(self):

        dados = Arquivo().quebrar_linhas()

        dic = {}

        for linha in dados:
            dic[linha[1]] = []
            if len(dic) == 3:
                break

        for linha in dados:
            if float(linha[3]) < 5.0:
                dic[linha[1]].extend([float(linha[3])])

        for ii in dic:
           total = len(ii)
           dic[ii] = total

        labels = [item for item in dic.keys()]
        tam = [item for item in dic.values()]

        fg1, ax = plt.subplots()

        ax.pie(tam, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        plt.title('Percentual de reprovação por curso')
        plt.savefig('reprovação_por_curso.png')

    def grf_reprova_p(self):
        
        dados = Arquivo().quebrar_linhas()
        
        dic = {}

        for linha in dados:
            dic[linha[2]] = []
            if len(dic) == 20:
                break

        for linha in dados:
            if float(linha[3]) < 5.0:
                dic[linha[2]].extend([float(linha[3])])

        for ii in dic:
           total = len(ii)
           dic[ii] = total

        labels = [item for item in dic.keys()]
        tam = [item for item in dic.values()]

        fg1, ax = plt.subplots()
        plt.rcParams['legend.fontsize'] = 7
        ax.pie(tam, labels=None, startangle=90)
        ax.legend(labels, title='Todos representam 5%', loc=5)
        ax.axis('equal')
        plt.title('Percentual de reprovação período')
        plt.margins(0.2)
        plt.subplots_adjust(left=0)
        plt.subplots_adjust(bottom=0.22)
        plt.subplots_adjust(right=1)
        plt.subplots_adjust(top=0.91)
        plt.savefig('reprovação_por_periodo.png')

    def grf_repro_all(self):

        dados = Arquivo().quebrar_linhas()
        
        dic = {'notas': []}
        total = {}

        for linha in dados:
            total[linha[0]] = []
            if float(linha[3]) < 5.0:
                dic['notas'].extend([float(linha[3])])

        total_rep = len(dic['notas'])
        total_matr = len(total.keys())
        total_matr -= total_rep

        label = ['Reprovações', 'Total de matrículas']
        tam = [total_rep,total_matr]

        fg1, ax = plt.subplots()
        plt.rcParams['legend.fontsize'] = 10

        ax.pie(tam, labels=None, startangle=90, autopct='%1.1f%%')
        ax.legend(label, title='Percentual de\nreprovações', loc=5,
                  bbox_to_anchor=(0.8,-0.5,0.5,1))
        plt.title('Gráfico do total de reprovações')
        plt.savefig('reprovações_totais.png')







a = Arquivo()
a.media_grau()
a.grau_por_curso()
a.maior_grau_p()
a.reprovados()
a.desistentes()        
a.grf_md_curso()
a.grf_md_pe()
a.grf_reprova_curso()
a.grf_reprova_p()
a.grf_repro_all()


