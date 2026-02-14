from main import classify

tests = [
    ## negativity
    ("bad", "bad, you did badly", "negativity"),
    ("bad in Lithuanian", "blogai, blogai padarei", "negativity"),
    ("poor", "you did poorly", "negativity"),
    ("terrible day", "this has been a terrible day", "negativity"),
    ("terrible in French", "c'est vraiment terrible, quelle horreur", "negativity"),
    ("bad in Japanese", "最悪だ、本当にひどい", "negativity"),
    ("awful in German", "das war schrecklich, einfach furchtbar", "negativity"),
    ## positivity
    ("good", "good, good job!", "positivity"),
    ("well", "you did well", "positivity"),
    ("beautiful day", "what a beautiful day it is", "positivity"),
    ("happy in Spanish", "estoy muy feliz, que dia tan bonito", "positivity"),
    ("joy in Korean", "너무 행복해요, 오늘 정말 좋은 날이에요", "positivity"),
    ("wonderful in Italian", "che bella giornata, sono contentissimo", "positivity"),
    ## praises
    ("excellent work", "excellent work on this project", "praises"),
    ("proud of you", "I am so proud of you", "praises"),
    ("nailed it", "you absolutely nailed it", "praises"),
    ("bravo in French", "bravo, travail magnifique", "praises"),
    ("well done in Portuguese", "muito bem, excelente trabalho", "praises"),
    ("great in Japanese", "素晴らしい仕事ですね、よくやった", "praises"),
    ## bullying
    ("insult", "you are such an idiot", "bullying"),
    ("exclusion", "nobody wants you here, go away", "bullying"),
    ("mockery", "everyone laughs at you behind your back", "bullying"),
    ("insult in Spanish", "eres un completo idiota, nadie te quiere", "bullying"),
    ("mockery in French", "t'es qu'un nul, tout le monde se moque de toi", "bullying"),
    ("insult in German", "du bist so ein Idiot, niemand mag dich", "bullying"),
    ## sarcasm
    ("oh really", "oh really, what a shocker", "sarcasm"),
    ("sure thing", "yeah right, sure thing buddy", "sarcasm"),
    ("slow clap", "wow, slow clap for that brilliant idea", "sarcasm"),
    ("sarcasm in French", "oh bien sur, quelle surprise incroyable", "sarcasm"),
    ("sarcasm in Spanish", "si claro, como si eso fuera verdad", "sarcasm"),
    ("sarcasm in German", "ja klar, was fuer eine Ueberraschung", "sarcasm"),
    ## gratitude
    ("thank you", "thank you so much for your help", "gratitude"),
    ("appreciate it", "I really appreciate everything you have done", "gratitude"),
    ("thanks in Spanish", "muchas gracias por todo", "gratitude"),
    ("thanks in French", "merci beaucoup pour tout, je vous suis reconnaissant", "gratitude"),
    ("thanks in Japanese", "本当にありがとうございます、感謝しています", "gratitude"),
    ("thanks in Portuguese", "muito obrigado por tudo que voce fez", "gratitude"),
    ## encouragement
    ("you can do it", "you can do it, I believe in you!", "encouragement"),
    ("keep going", "don't give up, keep pushing forward", "encouragement"),
    ("team spirit", "let's go team, we've got this!", "encouragement"),
    ("courage in French", "tu peux le faire, je crois en toi, courage", "encouragement"),
    ("go for it in Spanish", "tu puedes, no te rindas, adelante", "encouragement"),
    ("keep going in Japanese", "頑張って、あなたならできる", "encouragement"),
    ## humor
    ("lol", "lol that was hilarious", "humor"),
    ("joke", "why did the chicken cross the road", "humor"),
    ("haha", "haha I can't stop laughing", "humor"),
    ("funny in Spanish", "jajaja que gracioso, no puedo parar de reir", "humor"),
    ("funny in French", "mdr trop drole, je suis mort de rire", "humor"),
    ("funny in Korean", "ㅋㅋㅋ 너무 웃겨요, 배꼽 빠지겠어", "humor"),
    ## frustration
    ("annoyed", "ugh this is so annoying, nothing works", "frustration"),
    ("fed up", "I am so fed up with this nonsense", "frustration"),
    ("why", "why does this keep happening to me", "frustration"),
    ("frustrated in Spanish", "estoy harto, nada funciona, que rabia", "frustration"),
    ("frustrated in French", "j'en ai marre, rien ne marche, c'est insupportable", "frustration"),
    ("frustrated in Japanese", "もうイライラする、何もうまくいかない", "frustration"),
    ## curiosity
    ("how", "how does this work exactly?", "curiosity"),
    ("wonder", "I wonder what would happen if we tried that", "curiosity"),
    ("explain", "can you explain this to me?", "curiosity"),
    ("curious in Spanish", "como funciona esto exactamente?", "curiosity"),
    ("curious in French", "comment ca marche? je voudrais comprendre", "curiosity"),
    ("curious in Japanese", "これはどういう仕組みですか？教えてください", "curiosity"),
    ## toxicity
    ("threat", "I will find you and hurt you", "toxicity"),
    ("hate", "I hate everyone like you", "toxicity"),
    ("slur", "you disgusting piece of garbage, die", "toxicity"),
    ("threat in Spanish", "te voy a encontrar y te vas a arrepentir", "toxicity"),
    ("hate in French", "je te deteste, tu merites de souffrir", "toxicity"),
    ("threat in German", "ich werde dich finden und du wirst es bereuen", "toxicity"),
    ## emoji
    ("emoji 🎉", "🎉", "positivity"),
    ("emoji 😞", "😞", "negativity"),
    ("emoji 😂", "😂😂😂", "humor"),
    ("emoji ❤️", "❤️", "gratitude"),
    ("emoji 🤔", "🤔", "curiosity"),
    ## mixed signals
    ("sarcastic praise", "oh great job, really, what a genius move", "sarcasm"),
    ("backhanded compliment", "well you tried your best I guess", "praises"),
    ("polite frustration", "with all due respect, this is unacceptable", "negativity"),
    ("encouraging criticism", "you made a mistake but I know you can fix it", "encouragement"),
]

passed = 0
failed = 0

for label, text, expected in tests:
    scores = classify(text)
    top = max(scores, key=scores.get)
    top_score = scores[top]
    expected_score = scores[expected]
    ok = top == expected
    status = "PASS" if ok else "FAIL"

    if ok:
        passed += 1
        print(f"  {status}  {label:30s} -> {top:15s} ({top_score:.3f})")
    else:
        failed += 1
        print(f"  {status}  {label:30s} -> {top:15s} ({top_score:.3f})  expected {expected} ({expected_score:.3f})")

print(f"\n{passed}/{passed + failed} passed, {failed} failed")
