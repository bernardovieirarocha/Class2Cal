def write_templates():
    csv_content = "alias,full_name,professor,room,schedule_codes\nEDO,Equações Diferenciais Ordinárias,Prof. Silva,Sala 101,24M56\nCFVV2,Cálculo Vetorial e Variável Complexa,Prof. Souza,Sala 202,3T12\nAEDs3,Algoritmos e Estruturas de Dados III,Prof. Lima,Sala 303,56N12\n"
    with open('courses_template.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)
    json_content = {
        "semester": {
            "start_date": "YYYY-MM-DD",
            "end_date": "YYYY-MM-DD",
            "calendar_name": "CEFET-Semestre"
        },
        "courses": [
            {"alias": "EDO", "full_name": "Equações Diferenciais Ordinárias", "professor": "Prof. Silva", "room": "Sala 101", "schedule_codes": "24M56"},
            {"alias": "CFVV2", "full_name": "Cálculo Vetorial e Variável Complexa", "professor": "Prof. Souza", "room": "Sala 202", "schedule_codes": "3T12"},
            {"alias": "AEDs3", "full_name": "Algoritmos e Estruturas de Dados III", "professor": "Prof. Lima", "room": "Sala 303", "schedule_codes": "56N12"}
        ]
    }
    import json
    with open('courses_template.json', 'w', encoding='utf-8') as f:
        json.dump(json_content, f, ensure_ascii=False, indent=2)
