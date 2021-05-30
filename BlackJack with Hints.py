import random
#from art import logo
import pandas as pd
 
def game():
    #print(logo)
    cards=[]
    for j in range (2,12):
        cards.extend([j for k in range (0,4)]) 
    cards.extend([10 for k in range (0,3*4)])    
    print("Shuffling Cards")
    random.shuffle(cards)
    cards1=cards.copy()
    df=pd.read_excel("Blackjack_Stats.xlsx",index_col=None)
    def a (d):
        if sum(d)>21:
            if 11 in d:
                d[d.index(11)]=1  
        
    def game1(round1): 
        round1=round1+1
        player=[]
        dealer=[]              
        for k in range (0,2):
            player.append(cards.pop(0))
            dealer.append(cards.pop(0))
        a(player)
        a(dealer) 
        if sum(player)==21:
            print("Player has a Blackjack")
            if sum(dealer)==21:
                print("            ")
                print("Draw")
                return 0
            else:
                print("            ")
                print("Player Wins")   
                return 1
            print(f"Player Cards {*player,}")
            print(f"Dealer Cards {*dealer,}")
        else:    
            print(f"Player Cards {*player,}")       
            print("Dealer Cards "+str(dealer[0])+" _")
        df1=df[(df['Round']==round1) & (df['Sum_player_2']==sum(player))]
        df3=round(df1['Prob_Stand'].item()*100,1)
        print(f'In {df3} percent cases the player stood')
        K=int(input("Player 1-Hit 2-Stand "))
        while (K==1 and len(cards)>0):    
            player.append(cards.pop(0))
            a(player)
            if sum(player)>21:
                print("            ")
                print(f"Player Cards {*player,}") 
                print(f"Dealer Cards {*dealer,}")
                print("Dealer Wins")
                return -1
            else:
                print(f"Player Cards {*player,}")    
                K=int(input("Player 1-Hit 2-Stand "))
        print(f"Dealer Cards {*dealer,}")
        while(sum(dealer)<17 and len(cards)>0):
            dealer.append(cards.pop(0))
            a(dealer)
            print(f"Dealer Cards {*dealer,}")
        if sum(dealer)>sum(player) and sum(dealer)<=21:
            print("            ")
            print("Dealer Wins")
            print(f"Player Cards {*player,}") 
            print(f"Dealer Cards {*dealer,}")
            return -1
        if sum(dealer)>21 or sum(player)>sum(dealer):
            print("            ")
            print("Player Wins")
            print(f"Player Cards {*player,}") 
            print(f"Dealer Cards {*dealer,}")
            return 1
        if sum(player)==sum(dealer):
            print("            ")
            print("Draw")
            print(f"Player Cards {*player,}") 
            print(f"Dealer Cards {*dealer,}")
            return 0
    def best(cards):
        visited={}
        def win(player1,dealer1,b):
            if sum(player1)>21:
                return -1,b,dealer1
            if sum(player1)==21 and len(player1)==2:
                return 1,b,dealer1
            while (sum(dealer1)<17 and b<(len(cards)-1)):
                dealer1.extend([cards[b+1]])
                b=b+1
                if sum(dealer1)>21:
                    if 11 in dealer1:
                        dealer1[dealer1.index(11)]=1
            if sum(dealer1)>21 or sum(player1)>sum(dealer1) :        
               return 1,b,dealer1
            if sum(player1)==sum(dealer1):
                return 0,b,dealer1
            return -1,b ,dealer1         
        def DP(a):
            if a in visited:
                return visited[a][0]
            if a>len(cards)-4:
                return 0
            player=[]
            dealer=[]
            player.extend([cards[a],cards[a+2]])
            dealer.extend([cards[a+1],cards[a+3]])
            p=sum(player)
            s,b1,xc=win(player.copy(),dealer.copy(),a+3)
            pos=[]
            pos1=[]
            pos1.append([s,b1+1,player.copy(),xc.copy()])
            pos.extend([s+DP(b1+1)])
            
            for i in range (0,len(cards)-a-4):
                if p>=21:
                    break
                player.extend([cards[a+4+i]])
                p=sum(player)
                s,b1,xc=win(player.copy(),dealer.copy(),a+4+i)
                pos1.append([s,b1+1,player.copy(),xc.copy()])
                pos.extend([s+DP(b1+1)])
            zipped_lists = zip(pos, pos1)
            sorted_zipped_lists = sorted(zipped_lists,reverse=True)
            sorted_list1 = [element for _, element in sorted_zipped_lists]    
            visited[a]=[max(pos),sorted_list1[0]]     
            return max(pos)  
        ans=DP(0)  
        return(visited) 
    score=0
    visited=best(cards1)
    print(f'Max Score in this Deck {visited[0][0]}')
    f1=0
    while (len(cards)>=4):
        T=int(input("Want Hint? 1- Yes, 2-No "))
        if T==1:
            print(f'AI had asked for {len(visited[52-len(cards)][1][2])-2} hit')
        score=score+game1(f1)
        f1=f1+1
        if len(cards)>=4:
            print(f'Current Score {score}. Your max score can now only be {score+visited[52-len(cards)][0]}')
        else:
            print(f'Current Score {score}.')
        print("******************************************")
        print("            ")
    print(f'Final Score {score}')
    
    q=0
    c=1
    c1=0
    while (q in visited):
        print (visited[q][1][0],visited[q][1][1],visited[q][1][2],visited[q][1][3])
        c1=c1+visited[q][1][0]
        print (f'Score {c1} and AI had asked for {len(visited[q][1][2])-2} hit')
        q=visited[q][1][1]
        c=c+1
    print(f'Best score possible {c1} in moves {c}')
    print(cards1)
game()