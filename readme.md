# Trabalho de Conclusão de Curso II

## Tecnologias utilizadas
jupyter notebooks
python

## Instalação

Será utilizado o Python 3.6.8. Em ambiente linux:
sudo apt install python3 python3-pip jupyter

### Ambiente Virtual
sudo pip3 install virtualenv
python3 -m virtualenv tcc2
source tcc2/bin/activate

### Utilizando o conda
conda activate base
conda activate tcc
conda install <name>

### Rodando testes
Para rodar os testes que estão sendo executados na POC basta seguir o comando abaixo
python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions

## TODO
- [x] fazer uma poc da api da wikipedia
- [x] coletar páginas usando api da wikipedia
- [x] fazer poc do redirect
- [ ] coletar redirects das páginas com erro
- [ ] refactorar
- [ ] implementar redirect
- [ ] coletar os arquivos com erro com o redirect
- [ ] incorporar o redirect na coleta automaticamente
- [ ] coletar os conteúdos
- [ ] estruturar informações
- [ ] estudar a extração de features
- [ ] criar o extrator de features 
- [ ] extrair features
- [ ] fazer uma poc do modelo
- [ ] treinar o modelo