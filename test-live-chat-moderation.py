import sys
sys.argv = ['main.py', '--config', 'live-chat-moderation.yaml']
from main import classify

tests = [
    ## toxicity
    ("death threat", "I will find you and kill you", "toxicity"),
    ("violent threat", "you are going to pay for this, I will hurt you", "toxicity"),
    ("wish harm", "I hope you suffer and die", "toxicity"),
    ("threat in Spanish", "te voy a matar, vas a sufrir", "toxicity"),
    ("threat in French", "je vais te tuer, tu vas souffrir", "toxicity"),
    ("threat in German", "ich bringe dich um, du wirst leiden", "toxicity"),
    ## harassment
    ("insult", "you are such a pathetic loser", "harassment"),
    ("exclusion", "nobody wants you here, get lost", "harassment"),
    ("mockery", "everyone laughs at you, you are worthless", "harassment"),
    ("insult in Spanish", "eres un perdedor patetico, nadie te quiere", "harassment"),
    ("insult in French", "t'es qu'un nul, personne ne t'aime", "harassment"),
    ("insult in German", "du bist so erbaermlich, niemand mag dich", "harassment"),
    ## hate_speech
    ("go back", "go back to your country, immigrants are ruining everything", "hate_speech"),
    ("your kind", "your kind is not welcome here, your race is inferior", "hate_speech"),
    ("all the same", "all of your ethnicity are criminals, I hate your people", "hate_speech"),
    ("bigotry in Spanish", "tu raza es inferior, los inmigrantes arruinan todo", "hate_speech"),
    ("bigotry in French", "retourne dans ton pays, ta race est inferieure", "hate_speech"),
    ("bigotry in German", "deine Rasse ist minderwertig, Auslaender ruinieren alles", "hate_speech"),
    ## sexual_content
    ("solicitation", "send me nudes right now", "sexual_content"),
    ("explicit request", "let's sext, send me something dirty", "sexual_content"),
    ("unwanted advance", "I want to see you naked, show me everything", "sexual_content"),
    ("sexual in Spanish", "envíame fotos desnuda, quiero ver todo", "sexual_content"),
    ("sexual in French", "envoie moi des photos nues, je veux tout voir", "sexual_content"),
    ## spam
    ("promo link", "check out my channel and subscribe for free stuff", "spam"),
    ("giveaway", "free giveaway click this link to enter now", "spam"),
    ("discount code", "use my discount code for 50 percent off, buy now", "spam"),
    ("spam in Spanish", "visita mi pagina, suscribete gratis, ofertas increibles", "spam"),
    ("spam in French", "visitez mon site, cliquez ici pour des cadeaux gratuits", "spam"),
    ## profanity
    ("swearing", "what the fuck is this bullshit", "profanity"),
    ("cursing", "damn it, this is such crap", "profanity"),
    ("vulgar", "piss off you dumbass", "profanity"),
    ("profanity in Spanish", "maldita sea, que mierda es esta", "profanity"),
    ("profanity in French", "putain de merde, c'est quoi cette connerie", "profanity"),
    ## self_harm
    ("suicidal", "I don't want to be alive anymore, I want to end it", "self_harm"),
    ("hopeless", "nobody would miss me if I was gone", "self_harm"),
    ("cutting", "I have been hurting myself, I can't stop", "self_harm"),
    ("self harm in Spanish", "no quiero vivir mas, nadie me extrañaria", "self_harm"),
    ("self harm in French", "je ne veux plus vivre, personne ne me regrettera", "self_harm"),
    ## doxxing
    ("home address", "here is their home address, go find them", "doxxing"),
    ("phone number", "I'm posting their phone number for everyone to see", "doxxing"),
    ("real identity", "their real name is John Smith and they live on Oak Street", "doxxing"),
    ("doxxing in Spanish", "aqui esta su direccion, vayan a buscarlo", "doxxing"),
    ("doxxing in French", "voici son adresse personnelle et son numero de telephone", "doxxing"),
    ## scam
    ("password phish", "send me your password to verify your account", "scam"),
    ("money scam", "wire me money and I will double it, guaranteed", "scam"),
    ("credit card", "I need your credit card number to process the refund", "scam"),
    ("scam in Spanish", "envíame tu contraseña para verificar tu cuenta", "scam"),
    ("scam in French", "envoyez moi votre mot de passe pour verifier votre compte", "scam"),
    ## impersonation
    ("fake admin", "I am the admin, obey me and do as I say right now", "impersonation"),
    ("fake moderator", "this is the moderator speaking, obey the rules I set", "impersonation"),
    ("fake support", "I am a verified staff member, trust me I am in charge here", "impersonation"),
    ("impersonation in Spanish", "soy el administrador, obedezcan mis ordenes ahora", "impersonation"),
    ("impersonation in French", "je suis le moderateur officiel, obeissez moi", "impersonation"),
    ## raiding
    ("raid call", "everyone go spam their chat right now", "raiding"),
    ("brigade", "let's all raid this channel and flood their stream", "raiding"),
    ("coordinated attack", "everyone report their channel and troll their chat", "raiding"),
    ("raid in Spanish", "todos vayan a hacer spam en su chat ahora", "raiding"),
    ("raid in French", "allez tous spammer leur chat, on les raid", "raiding"),
    ## positive
    ("great stream", "great stream, love this community so much", "positive"),
    ("having fun", "this is so fun, best chat ever", "positive"),
    ("wholesome", "you are awesome, really enjoying the wholesome vibes", "positive"),
    ("positive in Spanish", "me encanta esta comunidad, que buen stream", "positive"),
    ("positive in French", "j'adore ce stream, cette communaute est geniale", "positive"),
    ("positive in Japanese", "最高の配信ですね、このコミュニティ大好き", "positive"),
    ## mixed signals
    ("polite scam", "hello friend, I just need your password to help you", "scam"),
    ("friendly spam", "hey everyone check out my awesome channel, subscribe please", "spam"),
    ("angry profanity", "what the hell is wrong with this damn thing", "profanity"),
    ("threatening doxx", "I know where you live and I will post your address", "doxxing"),
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
