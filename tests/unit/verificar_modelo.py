from joblib import load

conteudo = load("model/ddos_model.pkl")

print("[INFO] Tipo do conteúdo:", type(conteudo))
print(conteudo)
