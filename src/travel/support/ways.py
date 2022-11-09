"""
Nomes de vias para serem processados pelo gerador de informação
"""

# Tipo de via

VIA_ESTRADA = 'Estrada'
VIA_FERROVIA = 'Ferrovia'

# País

ANDORRA = "AD"
ESPANHA = "ES"
GIBRALTAR = "GI"
PORTUGAL = "PT"

# Auto-estradas e vias rápidas
#   (<Nome curto>, <Nome comprido segundo o OSM>, <País>)

ES_A1 = ("A-1", "Autovía del Norte", ESPANHA)
ES_A2 = ("A-2", "Autovía del Nordeste", ESPANHA)
ES_A3 = ("A-3", "Autovía del Este", ESPANHA)
ES_A4 = ("A-4", "Autovía del Sur", ESPANHA)
ES_A5 = ("A-5", "Autovía del Suroeste", ESPANHA)
ES_A6 = ("A-6", "Autovía del Noroeste", ESPANHA)
ES_A7 = ("A-7", "Autovía del Mediterráneo", ESPANHA)
ES_A8 = ("A-8", "Autovía del Cantábrico", ESPANHA)
ES_A10 = ("A-10", "Autovía de la Barranca", ESPANHA)
ES_A42 = ("A-42", "Autovía de Toledo", ESPANHA)
ES_A44 = ("A-44", "Autovía de Sierra Nevada-Costa Tropical", ESPANHA)
ES_A45 = ("A-45", "Autovía de Málaga", ESPANHA)
ES_A49 = ("A-49", "Autopista del Quinto Centenario", ESPANHA)
ES_A50 = ("A-50", "Autovía Ávila-Salamanca", ESPANHA)
ES_A52 = ("A-52", "Autovía de las Rías Baixas", ESPANHA)
ES_A55 = ("A-55", "Autovía do Atlántico", ESPANHA)
ES_A58 = ("A-58", "Autovía Trujillo-Cáceres", ESPANHA)
ES_A62 = ("A-62", "Autovía de Castilla", ESPANHA)
ES_A66 = ("A-66", "Autovía Ruta de la Plata", ESPANHA)
ES_A92 = ("A-92", "Autovía de Andalucía", ESPANHA)
ES_A92M = ("A-92M", "Autovía A-92 Málaga", ESPANHA)
ES_A92N = ("A-92N", "Autovía A-92 Norte", ESPANHA)
ES_A483 = ("A-483", "Bollullos-Matalascañas", ESPANHA)
ES_A497 = ("A-497", "Autovía de Huelva a Punta Umbría", ESPANHA)
ES_AP1 = ("AP-1", "Autopista del Norte", ESPANHA)
ES_AP2 = ("AP-2", "Autopista Zaragoza-Mediterráneo", ESPANHA)
ES_AP4 = ("AP-4", "Autopista del Sur", ESPANHA)
ES_AP6 = ("AP-6", "Autopista del Noroeste", ESPANHA)
ES_AP7 = ("AP-7", "Autopista del Mediterráneo", ESPANHA)
ES_AP8 = ("AP-8", "Autopista del Cantábrico", ESPANHA)
ES_AP9 = ("AP-9", "Autoestrada do Atlántico", ESPANHA)
ES_AP51 = ("AP-51", "Conexión Ávila", ESPANHA)
ES_AV20 = ("AV-20", "Circunvalación de Ávila", ESPANHA)
ES_EXA1 = ("EX-A1", "Autovía del Norte de Extremadura", ESPANHA)
ES_EXA2 = ("EX-A2", "Autovía de las Vegas Altas", ESPANHA)
ES_GR30 = ("GR-30", "Circunvalación de Granada", ESPANHA)
ES_H30 = ("H-30", "Ronda Exterior Norte", ESPANHA)
ES_M30 = ("M-30", "Autovía de Circunvalación M-30", ESPANHA)
ES_M40 = ("M-40", "Autopista de Circunvalación M-40", ESPANHA)
ES_M45 = ("M-45", "Autopista de Circunvalación M-45", ESPANHA)
ES_M50 = ("M-50", "Autopista de Circunvalación M-50", ESPANHA)
ES_R2 = ("R-2", "Radial R-2", ESPANHA)
ES_R3 = ("R-3", "Radial R-3", ESPANHA)
ES_R4 = ("R-4", "Radial R-4", ESPANHA)
ES_R5 = ("R-5", "Radial R-5", ESPANHA)

PT_A1 = ("A1", "Autoestrada do Norte", PORTUGAL)
PT_A2 = ("A2", "Autoestrada do Sul", PORTUGAL)
PT_A3 = ("A3", "Autoestrada de Entre-Douro-e-Minho", PORTUGAL)
PT_A4 = ("A4", "Autoestrada Transmontana", PORTUGAL)
PT_A5 = ("A5", "Autoestrada da Costa do Estoril", PORTUGAL)
PT_A6 = ("A6", "Autoestrada do Alentejo Central", PORTUGAL)
PT_A7 = ("A7", "Autoestrada do Douro", PORTUGAL)
PT_A8 = ("A8", "Autoestrada do Oeste", PORTUGAL)
PT_A8_1 = ("A8-1", "Circular Oriental de Leiria", PORTUGAL)
PT_A9 = ("A9 CREL", "Circular Regional Exterior de Lisboa (CREL)", PORTUGAL)
PT_A10 = ("A10", "Autoestrada do Ribatejo", PORTUGAL)
PT_A11 = ("A11", "Autoestrada do Baixo Minho", PORTUGAL)
PT_A12 = ("A12", "Autoestrada do Sul do Tejo", PORTUGAL)
PT_A13 = ("A13", "Autoestrada do Pinhal Interior", PORTUGAL)
PT_A13_1 = ("A13-1", "Radial de Coimbra", PORTUGAL)
PT_A14 = ("A14", "Autoestrada do Baixo Mondego", PORTUGAL)
PT_A15 = ("A15", "Autoestrada do Atlântico", PORTUGAL)
PT_A16 = ("A16", "Circular Exterior da Área Metropolitana de Lisboa", PORTUGAL)
PT_A17 = ("A17", "Autoestrada do Litoral Centro", PORTUGAL)
# A A18 está em projecto
PT_A19 = ("A19", "Variante da Batalha", PORTUGAL)
PT_A20 = ("A20", "Circular Regional Interior do Porto", PORTUGAL)
PT_A21 = ("A21", "Autoestrada de Mafra", PORTUGAL)
PT_A22 = ("A22", "Via do Infante", PORTUGAL)
PT_A23 = ("A23", "Autoestrada da Beira Interior", PORTUGAL)
PT_A24 = ("A24", "Autoestrada do Interior Norte", PORTUGAL)
PT_A25 = ("A25", "Autoestrada das Beiras Litoral e Alta", PORTUGAL)
PT_A26 = ("A26", "Autoestrada do Baixo Alentejo", PORTUGAL)
PT_A26_1 = ("A26-1", "Variante de Sines", PORTUGAL)
PT_A27 = ("A27", "Autoestrada do Vale do Lima", PORTUGAL)
PT_A28 = ("A28", "Autoestrada do Litoral Norte", PORTUGAL)
PT_A29 = ("A29", "Autoestrada da Costa de Prata", PORTUGAL)
# A A30 corresponde a um troço do IC2 em Lisboa
# A A31 corresponde a um troço do IC2 em Coimbra
PT_A32 = ("A32", "Autoestrada de Entre Douro-e-Vouga", PORTUGAL)
PT_A33 = ("A33", "Circular Regional Interior da Península de Setúbal (CRIPS)", PORTUGAL)
# A A34 corresponde a um troço do IC8 em Pombal
# A A35 corresponde ao IC12
# A A36 corresponde à IC17 CRIL
# A A37 corresponde ao IC19
# A A38 corresponde ao IC20
# A A39 corresponde ao IC21
# A A40 corresponde ao IC22
PT_A41 = ("A41 CREP", "Circular Regional Exterior do Porto", PORTUGAL)
PT_A42 = ("A42", "Autoestrada do Douro Litoral", PORTUGAL)
PT_A43 = ("A43", "Radial de Gondomar", PORTUGAL)
PT_A44 = ("A44", "Autoestrada de Vila Nova de Gaia", PORTUGAL)
PT_CSB = ("Circular Sul de Braga", "Circular Sul de Braga", PORTUGAL)
PT_IC17 = ("IC17 CRIL", "Circular Regional Interior de Lisboa (CRIL)", PORTUGAL)
PT_IC22 = ("IC22", "Radial de Odivelas", PORTUGAL)
PT_IC27 = ("IC27", "IC 27", PORTUGAL)
PT_VRI = ("VRI", "Via Regional Interior", PORTUGAL)

# Linhas ferroviárias
#   (<Nome segundo o OSM>, <País>, VIA_FERROVIA)
#   É essencial acrescentar VIA_FERROVIA no fim

ES_CERCANIAS_MADRID_C3 = ("Tren C-3: Chamartín -> Sol -> Atocha -> Aranjuez", ESPANHA, VIA_FERROVIA)
ES_CIUDAD_REAL_BADAJOZ = ("Ciudad Real-Badajoz", ESPANHA, VIA_FERROVIA)
ES_METRO_MADRID_LINHA_8 = ("Línea 8: Nuevos Ministerios-Aeropuerto T4", ESPANHA, VIA_FERROVIA)

PT_METRO_LISBOA_LINHA_VERMELHA = ("Linha Vermelha: São Sebastião → Aeroporto", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DA_BEIRA_ALTA = ("Linha da Beira Alta", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DA_BEIRA_BAIXA = ("Linha da Beira Baixa", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DE_BRAGA = ("Linha de Braga", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DE_CASCAIS = ("Linha de Cascais", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DE_CINTURA = ("Linha de Cintura", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DE_GUIMARAES = ("Linha de Guimarães", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DO_DOURO = ("Linha do Douro", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DO_LESTE = ("Linha do Leste", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DO_MINHO = ("Linha do Minho", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DO_OESTE = ("Linha do Oeste", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DO_NORTE = ("Linha do Norte", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DE_SINTRA = ("Linha de Sintra", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DO_SUL = ("Linha do Sul", PORTUGAL, VIA_FERROVIA)
PT_LINHA_DO_VOUGA = ("Linha do Vouga", PORTUGAL, VIA_FERROVIA)
PT_RAMAL_DE_ALFARELOS = ("Ramal de Alfarelos", PORTUGAL, VIA_FERROVIA)
PT_RAMAL_DE_BRAGA = ("Ramal de Braga", PORTUGAL, VIA_FERROVIA)
PT_RAMAL_DE_TOMAR = ("Ramal de Tomar", PORTUGAL, VIA_FERROVIA)
