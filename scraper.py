import os
import json
import requests
from bs4 import BeautifulSoup
import urllib3

# Disable annoying SSL warning messages in the GitHub Actions console
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

KEYWORDS = ["edital", "processo seletivo", "admissão", "inscriç", "vagas", "mestrado", "doutorado", "ingresso"]

# --- NATIONAL UNIVERSITY DIRECTORY ---
university_directory = [
    # --- NORTE ---
    {"name": "UEA - Hematologia", "url": "https://posgraduacao.uea.edu.br/hematologia/", "state": "AM", "region": "Norte"},
    {"name": "UEA - Ciências Humanas", "url": "https://posgraduacao.uea.edu.br/cienciashumanas/", "state": "AM", "region": "Norte"},
    {"name": "UEA - PPGLETRAS", "url": "https://ppgla.uea.edu.br", "state": "AM", "region": "Norte"},
    {"name": "UEA - Direito Ambiental", "url": "https://pos.uea.edu.br/direitoambiental", "state": "AM", "region": "Norte"},
    {"name": "UEA - ProfÁgua", "url": "https://pos.uea.edu.br/profagua/", "state": "AM", "region": "Norte"},
    {"name": "UEA - Ensino de Ciências", "url": "https://posgraduacao.uea.edu.br/ensinodeciencia/", "state": "AM", "region": "Norte"},
    {"name": "UEA - PPGED", "url": "https://posgraduacao.uea.edu.br/ppged/", "state": "AM", "region": "Norte"},
    {"name": "UEA - Segurança Pública", "url": "https://posgraduacao.uea.edu.br/segurancapublica/", "state": "AM", "region": "Norte"},
    {"name": "UEA - Dermatologia", "url": "https://posgraduacao.uea.edu.br/dermatologia/", "state": "AM", "region": "Norte"},
    {"name": "UEA - Portal Central", "url": "https://www.uea.edu.br/", "state": "AM", "region": "Norte"},
    {"name": "UEA - Biotecnologia", "url": "https://posgraduacao.uea.edu.br/biotecnologia/", "state": "AM", "region": "Norte"},
    {"name": "UEA - Proensp", "url": "https://www.proensp.com.br/", "state": "AM", "region": "Norte"},
    {"name": "UEA - PPGMT", "url": "https://ppgmt.uea.edu.br/", "state": "AM", "region": "Norte"},
    {"name": "UFAM - Enfermagem", "url": "https://ppgenf.ufam.edu.br/", "state": "AM", "region": "Norte"},
    {"name": "UFAM - Geografia", "url": "https://www.ppgg.ufam.edu.br/", "state": "AM", "region": "Norte"},
    {"name": "UFAM - Informática", "url": "https://ppgic.ufam.edu.br/", "state": "AM", "region": "Norte"},
    {"name": "UNIFAP - Educação", "url": "https://www2.unifap.br/ppged/", "state": "AP", "region": "Norte"},
    {"name": "UFPA - Educação", "url": "https://ppgeduc.propesp.ufpa.br/index.php/br/", "state": "PA", "region": "Norte"},
    {"name": "UFPA - Processos Estocásticos", "url": "https://ppgetno.propesp.ufpa.br/index.php/br/", "state": "PA", "region": "Norte"},
    {"name": "UFPA - Educação em Ciências", "url": "https://www.ppgecm.propesp.ufpa.br/index.php/br/", "state": "PA", "region": "Norte"},
    {"name": "UFPA - Biologia Ambiental", "url": "https://ppba.propesp.ufpa.br/index.php/br/", "state": "PA", "region": "Norte"},
    {"name": "UFPA - Saúde Animal", "url": "https://ppgsaam.propesp.ufpa.br/index.php/br/", "state": "PA", "region": "Norte"},
    {"name": "UFPA - Linguagem e Sociedade", "url": "https://www.pplsa.propesp.ufpa.br/index.php/br/", "state": "PA", "region": "Norte"},
    {"name": "UNIFESSPA - Planejamento", "url": "https://ppgpam.unifesspa.edu.br/", "state": "PA", "region": "Norte"},
    {"name": "UNIFESSPA - História", "url": "https://ppghistoria.unifesspa.edu.br", "state": "PA", "region": "Norte"},
    {"name": "UFRR - Comunicação", "url": "https://ufrr.br/ppgcom/", "state": "RR", "region": "Norte"},
    {"name": "UFRR - Letras", "url": "https://ufrr.br/ppgl/", "state": "RR", "region": "Norte"},
    {"name": "UFT - Engenharia de Alimentos", "url": "https://www.uft.edu.br/campus/palmas/cursos/pos-graduacao/mestrados-e-doutorados/ppgcta", "state": "TO", "region": "Norte"},
    {"name": "UFT - Produção Vegetal", "url": "https://www.uft.edu.br/campus/gurupi/cursos/pos-graduacao/mestrados-e-doutorados/ppgpv", "state": "TO", "region": "Norte"},

    # --- NORDESTE ---
    {"name": "UESC - Central", "url": "https://uesc.br", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Produção Vegetal", "url": "https://ppgpv.uesc.br/pt/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Ciências da Saúde", "url": "https://www.ppgcsuesc.com.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Microbiologia", "url": "https://www.uesc.br/microbiologia/", "state": "BA", "region": "Nordeste"},
    {"name": "UESB - Engenharia Florestal", "url": "https://www2.uesb.br/ppg/ppgef/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Enfermagem", "url": "https://www.uesc.br/ppgenf/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Letras", "url": "https://www.uesc.br/ppgl/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Economia", "url": "http://www.uesc.br/cursos/pos_graduacao/mestrado/ppgeconomia/index.php", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Ciências Ambientais", "url": "https://ppgca.uesc.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Zoologia", "url": "https://ppgzoo.uesc.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - História", "url": "https://www.uesc.br/ppgh/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Educação em Ciências", "url": "https://www.uesc.br/ppgecm/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Genética", "url": "https://www.ppggeneticauesc.com/", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Ecologia", "url": "https://www.uesc.br/ppgeca/", "state": "BA", "region": "Nordeste"},
    {"name": "UFSB - Estado e Sociedade", "url": "https://ufsb.edu.br/cfchs/pos-graduacao/ppges", "state": "BA", "region": "Nordeste"},
    {"name": "UFSB - Engenharia Civil/Ambiental", "url": "https://www.ufsb.edu.br/cftci/pos-graduacao/mestrado-em-engenharia-civil-e-ambiental", "state": "BA", "region": "Nordeste"},
    {"name": "UFOB - Arqueologia", "url": "https://sig.ufob.edu.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=920", "state": "BA", "region": "Nordeste"},
    {"name": "UFOB - Ciências Ambientais", "url": "https://ufob.edu.br/ppgact", "state": "BA", "region": "Nordeste"},
    {"name": "UFOB - Propriedade Intelectual", "url": "https://ufob.edu.br/ppgpi", "state": "BA", "region": "Nordeste"},
    {"name": "UESB - Genética e Biologia", "url": "https://www2.uesb.br/ppg/ppggbc2/", "state": "BA", "region": "Nordeste"},
    {"name": "UESB - Agronomia", "url": "https://www2.uesb.br/ppg/ppgagronomia/", "state": "BA", "region": "Nordeste"},
    {"name": "UESB - Educação", "url": "https://www2.uesb.br/ppg/ppged/", "state": "BA", "region": "Nordeste"},
    {"name": "UESB - Saúde Coletiva", "url": "https://www2.uesb.br/ppg/ppges/", "state": "BA", "region": "Nordeste"},
    {"name": "UESB - Ciências Ambientais", "url": "https://www2.uesb.br/ppg/ppgecfp/", "state": "BA", "region": "Nordeste"},
    {"name": "UFRB - Ciências Agrárias", "url": "https://ufrb.edu.br/pgcienciasagrarias/", "state": "BA", "region": "Nordeste"},
    {"name": "UFRB - Educação do Campo", "url": "https://www.ufrb.edu.br/ppgecid/", "state": "BA", "region": "Nordeste"},
    {"name": "UFRB - Gestão Pública", "url": "https://www.ufrb.edu.br/mpgestaoppss/", "state": "BA", "region": "Nordeste"},
    {"name": "UFRB - Arqueologia", "url": "https://www.ufrb.edu.br/ppgap/", "state": "BA", "region": "Nordeste"},
    {"name": "UFRB - Comunicação", "url": "https://www.ufrb.edu.br/ppgcom/en/", "state": "BA", "region": "Nordeste"},
    {"name": "UFRB - Engenharia Agrícola", "url": "https://www.ufrb.edu.br/ppgeec/", "state": "BA", "region": "Nordeste"},
    {"name": "UFRB - Artes", "url": "https://www.ufrb.edu.br/ppgartes/", "state": "BA", "region": "Nordeste"},
    {"name": "UFRB - Recursos Genéticos", "url": "https://www.ufrb.edu.br/pgrecvegetais/", "state": "BA", "region": "Nordeste"},
    {"name": "UEFS - Central", "url": "https://www.uefs.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UEFS - Letras", "url": "https://ppgel.uefs.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UEFS - Ecologia e Evolução", "url": "https://ecoevol.uefs.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UNEB - Letras", "url": "https://ppgels.uneb.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UNEB - Biociências", "url": "https://ppgmsb.uneb.br/index.html", "state": "BA", "region": "Nordeste"},
    {"name": "UNEB - Educação Física", "url": "https://ppgeduf.uneb.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UNEB - Crítica Cultural", "url": "https://www.poscritica.uneb.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UNEB - Ecologia Humana", "url": "https://ppgesa.uneb.br/", "state": "BA", "region": "Nordeste"},
    {"name": "UNEB - EJA", "url": "https://portal.uneb.br/tag/ppgeja/", "state": "BA", "region": "Nordeste"},
    {"name": "UFBA - Difusão do Conhecimento", "url": "https://difusao.dmmdc.ufba.br/pt-br", "state": "BA", "region": "Nordeste"},
    {"name": "UECE - Cuidados Clínicos", "url": "https://www.uece.br/ppcclis/", "state": "CE", "region": "Nordeste"},
    {"name": "UECE - Ciências Naturais", "url": "https://www.uece.br/ppgcn/", "state": "CE", "region": "Nordeste"},
    {"name": "UECE - Saúde Coletiva", "url": "https://www.uece.br/ppsac/", "state": "CE", "region": "Nordeste"},
    {"name": "UECE - Enfermagem", "url": "https://www.uece.br/ppgeen/", "state": "CE", "region": "Nordeste"},
    {"name": "UEMA - Agropecuária", "url": "https://www.ppgpdsa.uema.br/", "state": "MA", "region": "Nordeste"},
    {"name": "UEMA - Geografia", "url": "https://www.ppgeo.uema.br/", "state": "MA", "region": "Nordeste"},
    {"name": "UFCG - Recursos Naturais", "url": "https://recursosnaturais.ufcg.edu.br/", "state": "PB", "region": "Nordeste"},
    {"name": "UFCG - Meteorologia", "url": "https://ppgmet.ufcg.edu.br/index.php/pt/", "state": "PB", "region": "Nordeste"},
    {"name": "UFCG - Engenharia Elétrica", "url": "https://www.dee.ufcg.edu.br/pos-graduacao", "state": "PB", "region": "Nordeste"},
    {"name": "UPE - Enfermagem", "url": "https://w2.solucaoatrio.net.br/somos/upe-papgenf/index.php/pt/", "state": "PE", "region": "Nordeste"},
    {"name": "UPE - Hebiatria", "url": "https://w2.solucaoatrio.net.br/somos/upe-hebiatria/index.php/pt/", "state": "PE", "region": "Nordeste"},
    {"name": "UPE - Engenharia Civil", "url": "https://w2.solucaoatrio.net.br/somos/upe-ppgec/index.php/pt/", "state": "PE", "region": "Nordeste"},
    {"name": "UPE - Computação", "url": "https://pecpoli.com.br/", "state": "PE", "region": "Nordeste"},
    {"name": "UPE - Odontologia", "url": "https://w2.solucaoatrio.net.br/somos/upe-odontologia/index.php/pt/", "state": "PE", "region": "Nordeste"},
    {"name": "UFPE - Administração", "url": "https://www.ufpe.br/ppga", "state": "PE", "region": "Nordeste"},
    {"name": "UFPE - Ciências Farmacêuticas", "url": "https://www.ufpe.br/ppgcf", "state": "PE", "region": "Nordeste"},
    {"name": "UFPE - Economia", "url": "https://www.ufpe.br/ppgecon", "state": "PE", "region": "Nordeste"},
    {"name": "UFPE - Educação", "url": "https://www.ufpe.br/ppgeduc", "state": "PE", "region": "Nordeste"},
    {"name": "UFPE - Medicina Tropical", "url": "https://www.ufpe.br/ppgmedtrop", "state": "PE", "region": "Nordeste"},
    {"name": "UFRPE - Biometria", "url": "https://www.ppgbea.ufrpe.br/", "state": "PE", "region": "Nordeste"},
    {"name": "UFRPE - Ciências Florestais", "url": "https://www.ppgcf.ufrpe.br", "state": "PE", "region": "Nordeste"},
    {"name": "UFRPE - Engenharia Física", "url": "https://www.ppengfis.ufrpe.br/", "state": "PE", "region": "Nordeste"},
    {"name": "UFRPE - Fitopatologia", "url": "https://www.progel.ufrpe.br/", "state": "PE", "region": "Nordeste"},
    {"name": "UFRPE - Produção Vegetal", "url": "https://ww2.pgpv.ufrpe.br", "state": "PE", "region": "Nordeste"},
    {"name": "UNIVASF - Educação Física", "url": "https://portais.univasf.edu.br/ppgef", "state": "PE", "region": "Nordeste"},
    {"name": "UFPI - Portal Central", "url": "https://ufpi.br/", "state": "PI", "region": "Nordeste"},
    {"name": "UERN - Pós-Ensino", "url": "https://portal.uern.br/propeg/posensino/", "state": "RN", "region": "Nordeste"},
    {"name": "UFERSA - Fitotecnia", "url": "https://ppgfito.ufersa.edu.br/", "state": "RN", "region": "Nordeste"},
    {"name": "UFERSA - Direito", "url": "https://ppgd.ufersa.edu.br/", "state": "RN", "region": "Nordeste"},
    {"name": "UFS - Letras", "url": "https://www.sigaa.ufs.br/sigaa/public/programa/portal.jsf?id=135", "state": "SE", "region": "Nordeste"},

    # --- CENTRO-OESTE ---
    {"name": "IFGOIANO - Agroquímica", "url": "https://sistemas.ifgoiano.edu.br/sgcursos/index.php?id_curso=MTI=&p=pos-graduacao", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Bioparasitologia", "url": "https://bioparasitohospedeiro.iptsp.ufg.br", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Filosofia", "url": "https://pos.filosofia.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Física", "url": "https://posgraduacao.if.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Computação", "url": "https://ppgcc.inf.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Agronomia", "url": "https://ppgcta.agro.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Direito", "url": "https://ppgda.direito.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Direitos Humanos", "url": "https://pos.direitoshumanos.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Enfermagem", "url": "https://ppgenfs.fen.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Engenharia Civil", "url": "https://ppgeas.eeca.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - História", "url": "https://pos.historia.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Nutrição", "url": "https://ppgnut.fanut.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Odontologia", "url": "https://posgraduacao.odonto.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFG - Letras", "url": "https://pos.letras.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UFJ - Geografia", "url": "https://ppggeo.ufj.edu.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UnB - Nutrição Humana", "url": "https://ppgnh.unb.br/", "state": "DF", "region": "Centro-Oeste"},
    {"name": "UnB - Letras/Linguística", "url": "https://pgla.unb.br/", "state": "DF", "region": "Centro-Oeste"},
    {"name": "UnB - Psicologia", "url": "https://psto.unb.br/", "state": "DF", "region": "Centro-Oeste"},
    {"name": "UnB - Des. Sustentável", "url": "https://cds.unb.br/", "state": "DF", "region": "Centro-Oeste"},
    {"name": "UnB - Artes Visuais", "url": "https://www.ppgav.unb.br/", "state": "DF", "region": "Centro-Oeste"},
    {"name": "UnB - Ciência da Informação", "url": "https://ppgcinf.fci.unb.br", "state": "DF", "region": "Centro-Oeste"},
    {"name": "UnB - Medicina Tropical", "url": "https://medicinatropical.unb.br/", "state": "DF", "region": "Centro-Oeste"},
    {"name": "UNEMAT - Saúde Coletiva", "url": "https://tangaradaserra.unemat.br/faculdades/facabes/stricto/ppgasp/", "state": "MT", "region": "Centro-Oeste"},
    {"name": "UNEMAT - Ciências Ambientais", "url": "https://caceres.unemat.br/faculdades/facab/stricto/ppgca", "state": "MT", "region": "Centro-Oeste"},
    {"name": "UFMT - Antropologia Social", "url": "https://www.ufmt.br/curso/ppgas", "state": "MT", "region": "Centro-Oeste"},
    {"name": "UFMT - Estudos de Linguagem", "url": "https://www.ufmt.br/curso/ppgel", "state": "MT", "region": "Centro-Oeste"},
    {"name": "UFMT - Física", "url": "https://pgfa.ufmt.br", "state": "MT", "region": "Centro-Oeste"},
    {"name": "UFMT - Direito", "url": "https://ufmt.br/curso/ppgd/pagina/institucional/4111", "state": "MT", "region": "Centro-Oeste"},
    {"name": "UEMS - Recursos Naturais", "url": "https://www.uems.br/ppg/ppgdrs", "state": "MS", "region": "Centro-Oeste"},
    {"name": "UFMS - Administração", "url": "https://ppgad.ufms.br/", "state": "MS", "region": "Centro-Oeste"},
    {"name": "UFMS - Ciência Animal", "url": "https://ppgcianimal.ufms.br/", "state": "MS", "region": "Centro-Oeste"},
    {"name": "UFGD - Agronomia", "url": "https://portal.ufgd.edu.br/pos-graduacao/mestrado-doutorado-agronomia/index", "state": "MS", "region": "Centro-Oeste"},

    # --- SUL ---
    {"name": "UTFPR - Química", "url": "https://www.utfpr.edu.br/cursos/programas-de-pos-graduacao/ppgqb-td", "state": "PR", "region": "Sul"},
    {"name": "UTFPR - Biotecnologia", "url": "https://www.utfpr.edu.br/cursos/programas-de-pos-graduacao/ppgbiotec-multi", "state": "PR", "region": "Sul"},
    {"name": "UTFPR - Des. Regional", "url": "https://www.utfpr.edu.br/cursos/programas-de-pos-graduacao/ppgdr-pb", "state": "PR", "region": "Sul"},
    {"name": "UTFPR - Engenharia Elétrica", "url": "https://www.utfpr.edu.br/cursos/programas-de-pos-graduacao/cpgei-ct", "state": "PR", "region": "Sul"},
    {"name": "UFPR - Engenharia de Produção", "url": "http://www.ppgep.ufpr.br", "state": "PR", "region": "Sul"},
    {"name": "UFPR - Contabilidade", "url": "http://www.prppg.ufpr.br/site/ppgcontabilidade/", "state": "PR", "region": "Sul"},
    {"name": "UFPR - Engenharia Elétrica", "url": "http://www.eletrica.ufpr.br/ppgee", "state": "PR", "region": "Sul"},
    {"name": "UEL - Engenharia Elétrica", "url": "https://pos.uel.br/meel/", "state": "PR", "region": "Sul"},
    {"name": "UEL - Educação", "url": "https://www.ppedu.uel.br/pt/", "state": "PR", "region": "Sul"},
    {"name": "FURG - Computação", "url": "https://ppgcomp.furg.br/", "state": "RS", "region": "Sul"},
    {"name": "FURG - Letras", "url": "https://ppgletras.furg.br/", "state": "RS", "region": "Sul"},
    {"name": "FURG - Aquicultura", "url": "https://ppgaquicultura.furg.br/", "state": "RS", "region": "Sul"},
    {"name": "UFPEL - Veterinária", "url": "https://wp.ufpel.edu.br/ppgveterinaria/", "state": "RS", "region": "Sul"},
    {"name": "UFCSPA - Hepatologia", "url": "https://ufcspa.edu.br/vida-academica/pos-graduacao/mestrado-e-doutorado/hepatologia", "state": "RS", "region": "Sul"},
    {"name": "UFSM - Direito", "url": "https://www.ufsm.br/cursos/pos-graduacao/santa-maria/ppgd", "state": "RS", "region": "Sul"},
    {"name": "UFRGS - Informática", "url": "https://www.ufrgs.br/ppgcin/", "state": "RS", "region": "Sul"},

    # --- SUDESTE ---
    {"name": "UFES - Ciências Contábeis", "url": "https://cienciascontabeis.ufes.br/pt-br/pos-graduacao/PPGCC", "state": "ES", "region": "Sudeste"},
    {"name": "UFES - Engenharia Civil", "url": "https://engenhariacivil.ufes.br/pt-br/pos-graduacao/PPGEC", "state": "ES", "region": "Sudeste"},
    {"name": "UFU - Agronomia", "url": "https://ppgagro.iciag.ufu.br", "state": "MG", "region": "Sudeste"},
    {"name": "UFSJ - Biotecnologia", "url": "https://ufsj.edu.br/ppgbiotec/", "state": "MG", "region": "Sudeste"},
    {"name": "UFTM - Serviço Social", "url": "https://www.uftm.edu.br/stricto-sensu/ppgas", "state": "MG", "region": "Sudeste"},
    {"name": "UFV - Engenharia Civil", "url": "https://posengenhariacivil.ufv.br/", "state": "MG", "region": "Sudeste"},
    {"name": "UFJF - História", "url": "https://www2.ufjf.br/ppghistoria/", "state": "MG", "region": "Sudeste"},
    {"name": "UFLA - Administração", "url": "https://sigaa.ufla.br/sigaa/public/programa/apresentacao.jsf?lc=pt_BR&id=1787", "state": "MG", "region": "Sudeste"},
    {"name": "UNIFAL - Biotecnologia", "url": "https://www.unifal-mg.edu.br/ppgbiotec/", "state": "MG", "region": "Sudeste"},
    {"name": "UEMG - Artes", "url": "https://pos.uemg.br/ppgartes", "state": "MG", "region": "Sudeste"},
    {"name": "UFMG - Biologia Celular", "url": "http://pgbiologiacelular.icb.ufmg.br/", "state": "MG", "region": "Sudeste"},
    {"name": "UFOP - Engenharia Mineral", "url": "https://nugeo.ufop.br/", "state": "MG", "region": "Sudeste"},
    {"name": "CEFET-MG - Engenharia Civil", "url": "http://www.ppgec.cefetmg.br", "state": "MG", "region": "Sudeste"},
    {"name": "CEFET-RJ - Produção", "url": "https://dippg.cefet-rj.br/pppro/", "state": "RJ", "region": "Sudeste"},
    {"name": "UFRRJ - Fitotecnia", "url": "https://cursos.ufrrj.br/posgraduacao/ppgfba/", "state": "RJ", "region": "Sudeste"},
    {"name": "UNIFESP - Educação", "url": "https://ppg.unifesp.br/educacao/en/", "state": "SP", "region": "Sudeste"},
    {"name": "UFSCAR - Terapia Ocupacional", "url": "https://www.ppgto.ufscar.br/pt-br/ppgto-programa-de-pos-graduacao-em-terapia-ocupacional", "state": "SP", "region": "Sudeste"},
    {"name": "Unicamp - Engenharia de Alimentos", "url": "https://fea.unicamp.br/pos-graduacao/engenharia-de-alimentos/", "state": "SP", "region": "Sudeste"},
    {"name": "UNESP - Química", "url": "https://www.ibilce.unesp.br/#!/pos-graduacao/programas-de-pos-graduacao/quimica", "state": "SP", "region": "Sudeste"}
]

def fetch_page_html(url):
    """Safely fetches page HTML bypassing SSL verification bottlenecks."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=12, verify=False)
        return response.text if response.status_code == 200 else None
    except Exception as e:
        print(f"⚠️ Connection dropped for {url}: {e}")
        return None

def extract_academic_links(html, base_url):
    """Parses text assets and context anchors while dropping massive binary file payloads."""
    soup = BeautifulSoup(html, 'html.parser')
    valid_discoveries = []
    
    for anchor in soup.find_all('a', href=True):
        href_url = anchor['href']
        text_context = anchor.get_text().strip().lower()
        
        # Skip heavy media assets entirely
        if any(href_url.lower().endswith(ext) for ext in ['.pdf', '.zip', '.rar', '.docx', '.xlsx']):
            continue
            
        if any(keyword in text_context for keyword in KEYWORDS):
            full_link = href_url if href_url.startswith('http') else base_url.rstrip('/') + '/' + href_url.lstrip('/')
            valid_discoveries.append({"title": anchor.get_text().strip(), "link": full_link})
            
    return valid_discoveries

def analyze_program_status(link_url):
    """Heuristic assessment engine parsing active targets."""
    html = fetch_page_html(link_url)
    if not html:
        return "Check Portal", "See Website"
        
    html_lower = html.lower()
    
    # Check simple status flags
    if "inscrições abertas" in html_lower or "prorrogado" in html_lower:
        status = "Open"
    elif "encerrado" in html_lower or "inscrições encerradas" in html_lower:
        status = "Closed"
    else:
        status = "Check Portal"
        
    # Standard deadline regex search simulation
    deadline = "See Website"
    for word in html_lower.split():
        if "/" in word and len(word) >= 8:
            clean_word = "".join(c for c in word if c.isdigit() or c == "/")
            if len(clean_word) == 10:
                deadline = clean_word
                break
                
    return status, deadline

def run_scraper_engine():
    print(f"🚀 Initializing crawling matrix across {len(university_directory)} targets...")
    compiled_results = []
    uid = 1
    
    for uni in university_directory:
        print(f"Analyzing: {uni['name']} ({uni['state']})")
        page_content = fetch_page_html(uni['url'])
        
        if not page_content:
            continue
            
        found_links = extract_academic_links(page_content, uni['url'])
        
        if found_links:
            primary_discovery = found_links[0]
            status, deadline = analyze_program_status(primary_discovery['link'])
            
            compiled_results.append({
                "id": uid,
                "university": uni['name'],
                "program": primary_discovery['title'] if len(primary_discovery['title']) > 5 else "Processo Seletivo Regular",
                "region": uni['region'],
                "state": uni['state'],
                "status": status,
                "deadline": deadline,
                "link": primary_discovery['link']
            })
            uid += 1
            
    # Save clean data output file back into workspace environment
    output_filename = "discovered_programs.json"
    with open(output_filename, "w", encoding="utf-8") as file:
        json.dump(compiled_results, file, ensure_ascii=False, indent=2)
        
    print(f"🎉 Run successful. Data mapped and committed to {output_filename}")

if __name__ == "__main__":
    run_scraper_engine()