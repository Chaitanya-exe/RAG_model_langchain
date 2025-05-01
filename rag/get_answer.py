from .chains import userChains

def prepare_answer(user_question):
    chain = userChains[0]

    res = chain.invoke(input=user_question)

    return res