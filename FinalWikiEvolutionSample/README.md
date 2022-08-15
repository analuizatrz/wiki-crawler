# Wiki evolution: Wikipedia english revision articles represented through quality atributes

## Abstract

This paper presents the creation and publishing of the Wikipedia article's evolution dataset. This dataset is a set of revisions of articles, represented by quality attributes and quality classification. This dataset can be used for studies regarding automatic quality classification that consider the article revision history as well as understanding how the content and quality of articles evolve over time in this collaborative platform.

## Introdução

Este artigo descreve a criação e disponibilização da base de dados de evolução de artigos da Wikipédia. A base é caracterizada por atributos de qualidades e a classe de qualidade dos artigos em determinada data, sendo cada instância entendida como revisão. Esta base pode ser utilizada para estudos relacionados com classificação automática de qualidade que considerem o histórico de revisão do artigo e entendimento de como o conteúdo e qualidade dos artigos evoluem ao longo do tempo nessa plataforma colaborativa.

## Dataset

link para o dataset: https://figshare.com/articles/dataset/FinalWikiEvolutionSample_csv/20154434


## Atributos e Metadados da revisão

As revisões foram representadas por meio de atributos criados a partir dos respectivos conteúdos das revisões são baseados nos atributos de textos apresentados por Dalip (2009)[^1]. Esses atributos são divididos em três subgrupos: tamanho, estilo e estrutura.

### Atributos de Tamanho

O primeiro subgrupo é o subgrupo de tamanho que visa quantificar o conteúdo de uma revisão com base em quantidade de caracteres, palavras ou frases. A intuição por trás dos atributos de tamanho é que um artigo bom e maduro provavelmente não é tão curto, que pode indicar uma cobertura pobre sobre o tema, nem excessivamente longo, que pode indicar uma escrita verborrágica[^1]. Os atributos dessa subcategoria utilizados neste trabalho são apresentados na tabela abaixo:

| Coluna | Nome |
|---|---|
| Char Count | Quantidade de caracteres, incluindo espaços | 
| Word Count | Quantidade de palavras |
| Phrase count | Quantidade de frases |

### Atributos de estrutura

Os atributos de estrutura, por sua vez, indicam quão bem o artigo está organizado. De acordo com os padrões de qualidade da [Wikipédia](http://en.wikipedia.org/wiki/Wikipedia:Version_1.0_Editorial_Team/Release_Version_Criteria). Um bom artigo deve ser organizado de modo que seja claro, visualmente adequado e forneça as referências e materiais adicionais necessários. Os atributos de estrutura buscam descrever a estrutura do artigo, na tentativa de representar sua organização de seções, uso de imagens, ligações e citações [^1]. Os atributos dessa subcategoria utilizados neste trabalho são apresentados na tabela abaixo:

| Coluna | Nome | Detalhes |
|---|---| --- |
| Section count | Quantidade de seções | um bom artigo é organizado em seções, sendo esperado em particular na Wikipédia que o artigo contenha introdução, sumário, lista de referências e ligações externos |
| Mean section size | Tamanho médio das seções| é razão entre o número de caracteres das seções e a quantidade de seções |
| Shortest section size | Tamanho da menor seção | ajuda a detectar tamanho incomum, como seções vazias ou muito pequenas |
| Largest section size | Tamanho da maior seção | ajuda a detectar tamanho incomum, como seções que deveriam ser divididas | 
| Standard deviation of the section size | Desvio padrão do tamanho das seções | representa quão balanceadas são as seções | 
| Subsection Count | Quantidade de subseções | um bom artigo é organizado em seções, sendo esperado em particular na Wikipédia que o artigo contenha introdução, sumário, lista de referências e ligações externos |
| Mean subsection size| Tamanho médio das subseções | |
| Complete URL link count | Quantidade de ligação URL completas | quantidade de tags HTML 'a' nas quais o atributo 'href' se refere a um URL completo |
| Complete URL link count per section | Quantidade de ligações URL completas por seção | razão entre quantidade de ligação URL completas e subseções |
| Complete URL link count per length | Quantidade de ligações URL completas por tamanho | razão entre quantidade de ligação URL completas e tamanho do texto |
| Relative URL link count | Quantidade de ligações URL relativas | quantidade de tags HTML 'a' nas quais o atributo 'href' se refere a um URL relativo (por exemplo /images/cow.gif). |
| Relative URL link count per section | Quantidade de ligações URL relativa por seção | razão entre quantidade de ligação URL relativa e subseções |
| Relative URL link count per length | Quantidade de ligações URL relativa por tamanho | razão entre quantidade de ligação URL relativa e tamanho |
| Same page link count | Quantidade de ligações URL da mesma página | quantidade ligações que se referem a algum outro elemento na mesma página. Em outras palavras, quantidade de tags HTML 'a' nas quais 'href' aponta para algum ID da página html. Por exemplo, o valor '#mainDiv' aponta para um elemento na página cujo ID é 'mainDiv' |
| Same page link count per section | Quantidade de ligações URL da mesma página por seção | razão entre quantidade de ligações URL da mesma página e quantidade de subseções |
| Same page link count per length | Quantidade de ligações URL da mesma página por tamanho | razão entre quantidade de ligações URL da mesma página e tamanho |
| Images count | Quantidade de imagens | o uso de figura contribui para criar um conteúdo mais claro e visualmente agradável |
| Images per length | Média de imagens por seção | |
| Images per section | Quantidade de imagens por seção | razão entre quantidade de imagens e subseção |
| Images per subsection | Média de imagens por subseção | |
| Paragraph count | Quantidade de parágrafos | |
| Large paragraph count | Quantidade de parágrafos longos | |
| Large phrase count | Quantidade de frases longas | |

### Atributos de estilo

Os atributos de estilo têm como objetivo capturar o tipo de escrita do autor, por meio do uso de palavras. A ideia é que os artigos bons provavelmente apresentam característica distinguíveis de estilo.  Os atributos dessa subcategoria utilizados neste trabalho são apresentados na tabela abaixo:

| Coluna | Nome | Detalhes |
|---|---| --- |
| Largest phrase size | Tamanho da maior frase | número de palavras da maior frase. |
| Large phrase rate | Taxa de frases longas | Percentual das frases em que o tamanho é dez palavras maior que o tamanho médio |
| Short phrase rate | Taxa de frases curtas | Percentual das frases em que o tamanho é cinco palavras menor que o tamanho médio  |
| Auxiliary verbs count | Quantidade de verbos auxiliares (da língua inglesa) | por exemplo *be*, *do*, *have*, *will* |
| Interrogative pronouns count | Quantidade de pronomes interrogativos* (da língua inglesa) | por exemplo *who*, *whom*, *what*, *where* |
| Pronouns count | Quantidade de pronomes (da língua inglesa) | por exemplo *I*, *you*, *he*, *she* |
| Coordination conjunctions count | Quantidade de conjunções coordenativas (da língua inglesa) | por exemplo *and*, *but*, *so*, *yet* |
| Correlative conjunctions count | Quantidade de conjunções correlativas (da língua inglesa) | por exemplo *either*/*or*, *as*/*as*, *rather*/*than* |
| Subordinating conjunctions count | Quantidade de conjunções subordinativas (da língua inglesa) | por exemplo *while*, *when*, *whenever*, *once*, *after*, *before* |
| Articles count | Quantidade de artigos (da língua inglesa) | |
| Indefinite pronouns count | Quantidade de pronomes (da língua inglesa) | |
| Relative pronoums count | Quantidade de pronomes relativos (da língua inglesa) | |
| Prepositions count | Quantidade de preposições (da língua inglesa) | por exemplo *for*, *to*, *since*, *with* |
| To be verbs count | Quantidade de verbos ser/estar | verbos *to be* da língua inglesa, por exemplo *is*, *am* |
| Sentences starting with articles | Quantidade de frases que começam com artigos | |
| Sentences starting with auxiliary verbs | Quantidade de frases que começam com verbos auxiliares | |
| Sentences starting with coordination conjunctions | Quantidade de frases que começam com conjunções coordenativas | |
| Sentences starting with correlative conjunctions | Quantidade de frases que começam com conjuções correlativas | |
| Sentences starting with indefinite pronouns | Quantidade de frases que começam com pronomes indefinidos | |
| Sentences starting with interrogative pronouns | Quantidade de frases que começam com pronomes interrogativos | |
| Sentences starting with prepositions | Quantidade de frases que começam com preposições | |

### Referências

[^1]: Hasan Dalip, D., André Gonçalves, M., Cristo, M., and Calado, P. (2009). Automatic quality assessment of content created collaboratively by web communities: A case study of wikipedia. In Proceedings of the 9th ACM/IEEE-CS Joint Conference on Digital Libraries, JCDL ’09, pages 295–304, New York, NY, USA. ACM.

[^2]: Pinto, A. C., Silva, B. S., Carmo, P. R. M., Lima, R. L. A., Amorim, L. S. P., Viana, R. T. C., Dalip, D. H., and Oliveira, P. A. C. (2020). Webfeatures: A web tool to extract features from collaborative content. In Anais Estendidos do XXVI Simpósio Brasileiro de Sistemas Multimídia e Web, pages 103–106, Porto Alegre, RS, Brasil. SBC


