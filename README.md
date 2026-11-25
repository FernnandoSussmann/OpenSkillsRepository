# OpenSkillsRepository
Um repositório para colocar as skills que quero deixar públicas

# Skills
As skills estão na pasta `skills`. Por enquanto não tenho pretensão de criar um instalador. Consulte a maneira de instalar indicada na ferramenta que utiliza.

|skill|descrição|
|-----|---------|
|design-doc-creator| Cria Design Doc de uma feature|
|task-creator| Cria as tasks necessárias para implementar uma Design Doc. Busca indicar como paralelizar a implementação da mesma|
|implement-step| Implementa uma especificação procurando diferenciar o Agente que implementa, testa e verifica o que foi feito. Ao final da implementação abre um PR|
|implement-all-steps| Implementa todas as tasks em uma pasta da mesma forma que o `implement-step` faz|
|confia-task-workflow| A partir de uma Design Doc executa a `task-creator` com o Opus 5.5 high effort e `implement-all-steps` com o Sonnet 5.5 medium effort|
|usage-guard| Skill **experimental** gerada pelo ClaudeCode e especifica para ele. Verifica a porcentagem de uso da cota da conta ultrapassou 80% e caso isso aconteça para o processo até ela resetar para evitar que a execução falhe. A atualização não é tão frequente e para isso a skill utiliza os scripts da pasta `scripts`|

Nota: O texto da design-doc-creator.md que define o que é e as características de uma design doc foi retirada de um site, porém não consigo mais achá-lo. Suspeito que tenha sido uma versão antiga do https://www.designdocs.dev/.
