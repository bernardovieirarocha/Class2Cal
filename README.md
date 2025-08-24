
# Class2Cal


Automatize a criação de arquivos iCalendar (.ics) com horários acadêmicos a partir de CSV ou JSON, compatível com Apple Calendar, Google Calendar e outros.

## Instalação

Requer Python 3.10+.

```bash
python3 -m pip install python-dateutil  # opcional, se quiser usar dateutil
```

## Uso


### Interface gráfica para criar CSV/JSON intuitivamente

Execute o seguinte comando para abrir a interface gráfica:

```bash
python3 class2cal/app.py
```

Na janela, preencha os campos das disciplinas e clique em "Adicionar disciplina". Você pode salvar todas as disciplinas em um arquivo CSV ou JSON usando os botões correspondentes. No caso do JSON, será solicitado preencher os dados do semestre.

Use o arquivo gerado normalmente com a CLI para criar o .ics.



### Gerar templates de exemplo
```bash
python3 -m class2cal --write-templates
```
Cria `courses_template.csv` e `courses_template.json`.

### Gerar .ics a partir de CSV
```bash
python3 -m class2cal --csv cursos.csv --start 2025-08-04 --end 2025-12-10 --cal-name "Semestre 2025-2" --out materias.ics
```

### Gerar .ics a partir de JSON
```bash
python3 -m class2cal --json cursos.json
```

### Excluir datas específicas (feriados, greves)
```bash
python3 -m class2cal --csv cursos.csv --exdates 2025-09-07,2025-10-12
```

## Formato dos dados

### CSV
```
alias,full_name,professor,room,schedule_codes
EDO,Equações Diferenciais Ordinárias,Prof. Silva,Sala 101,24M56
CFVV2,Cálculo Vetorial e Variável Complexa,Prof. Souza,Sala 202,3T12
AEDs3,Algoritmos e Estruturas de Dados III,Prof. Lima,Sala 303,56N12
```

### JSON
```json
{
  "semester": {
    "start_date": "2025-08-04",
    "end_date": "2025-12-10",
    "calendar_name": "CEFET 2025-2"
  },
  "courses": [
    {"alias": "EDO", "full_name": "Equações Diferenciais Ordinárias", "professor": "Prof. Silva", "room": "Sala 101", "schedule_codes": "24M56"},
    {"alias": "CFVV2", "full_name": "Cálculo Vetorial e Variável Complexa", "professor": "Prof. Souza", "room": "Sala 202", "schedule_codes": "3T12"},
    {"alias": "AEDs3", "full_name": "Algoritmos e Estruturas de Dados III", "professor": "Prof. Lima", "room": "Sala 303", "schedule_codes": "56N12"}
  ]
}
```

## Testes

```bash
python3 -m unittest discover cefet2ics/tests
```


## Arquitetura
- `__main__.py`: CLI
- `parser.py`: parsing CSV/JSON
- `cefet_code.py`: parsing dos códigos de horários
- `timetable.py`: cálculo de datas/horários
- `ics_writer.py`: geração do .ics
- `templates.py`: templates de exemplo
- `app.py`: interface gráfica completa
- `tests/`: testes unitários


## Critérios de aceite
- Gera .ics compatível com Apple Calendar, Google Calendar e Outlook.
- Alias no título, nome completo/professor/sala nas notas.
- Múltiplos códigos por disciplina funcionam.
- Validações amigáveis, sem abortar toda execução.
- Arquivo .ics abre sem warnings nos principais calendários.
