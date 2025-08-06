```zsh
(base) mekann@MekannMacBook learning/learning-gh $ gp --set-upstream origin main
branch 'main' set up to track 'origin/main'.
Everything up-to-date
(base) mekann@MekannMacBook learning/learning-gh $ gh repo view                 
(base) mekann@MekannMacBook learning/learning-gh $ gh issue list
no open issues in Mekann2904/learning-gh

(base) mekann@MekannMacBook learning/learning-gh $ gh config set editor vim
(base) mekann@MekannMacBook learning/learning-gh $ gh issue create 

Creating issue in Mekann2904/learning-gh

? Title (required) テスト
? Body <Received>
? What's next? Submit
https://github.com/Mekann2904/learning-gh/issues/1
(base) mekann@MekannMacBook learning/learning-gh $ gh issue comment 1  
- Press Enter to draft your comment in vim... 
? Submit? Yes
https://github.com/Mekann2904/learning-gh/issues/1#issuecomment-3157733646
(base) mekann@MekannMacBook learning/learning-gh $ gh issue list     
(base) mekann@MekannMacBook learning/learning-gh $ gh issue view 1
(base) mekann@MekannMacBook learning/learning-gh $ gh issue comment 1
- Press Enter to draft your comment in vim... 
? Submit? Yes
https://github.com/Mekann2904/learning-gh/issues/1#issuecomment-3157738790
(base) mekann@MekannMacBook learning/learning-gh $ gh issue close 1  
✓ Closed issue Mekann2904/learning-gh#1 (テスト)
(base) mekann@MekannMacBook learning/learning-gh $ gh issue view   
accepts 1 arg(s), received 0
(base) mekann@MekannMacBook learning/learning-gh $ gh issue list
no open issues in Mekann2904/learning-gh
(base) mekann@MekannMacBook learning/learning-gh $ gh issue list --state all 
``` 
