import take_srn
import get_ysn

def main(inn):
    get_ysn.main()
    return take_srn.main(inn)

if __name__ == '__main__':
    main()


