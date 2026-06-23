from agent import conversar

print("HR Buddy (LangChain) — digite 'sair' para encerrar\n")
session_id = "cli-test"

while True:
    pergunta = input("Você: ")
    if pergunta.strip().lower() in ("sair", "exit", "quit"):
        print("Encerrando.")
        break
    resposta = conversar(pergunta, session_id)
    print(f"HR Buddy: {resposta}\n")
