import RecupLienMal as rlm
import GetPage as gp

def export_txt(texte,nom):
    with open("donneMAL/"+nom+".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(texte))

lien_mal=rlm.get_url_mal(1)
for lien in lien_mal:
    data=gp.get_data_page(lien)
    export_txt(data,lien.strip('/').split('/')[-1])