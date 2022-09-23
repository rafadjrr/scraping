import twitter as twitter
import bcv as bcv

def main():
    print('===== twitter ====')
    twitter.twitter()
    print('========== BCV ==========')
    try:
        bcv.bcv()
    except Exception as e:
        print("Problemas con el servidor destino => BCV", e)

main()