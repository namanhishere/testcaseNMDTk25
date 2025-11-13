EXECUTABLE_PATH = "./out.exe"
import subprocess
import itertools
import sys




def get_expected_output(slayerLevel, hp, breathingMastery, hasTalisman, timeOfDay, demonPresence, demonRank, swordSharpness, allyCount, bossHP, totalDamage, specialMoveReady):
    result = [] 

    
    power = (slayerLevel * 10) + (hp / 10) + (breathingMastery * 50)
    rank = ""
    if power >= 120:
        rank = "Hashira"
    elif 80 <= power < 120:
        rank = "Elite"
    else:
        rank = "Novice"
    result.append(f"[Scene 1] Rank: {rank} (power = {power:.1f})")

    
    scene2_status = ""
    if hasTalisman == 0:
        scene2_status = "Denied: No talisman."
    elif timeOfDay != 'D' and timeOfDay != 'N':
        scene2_status = "Warning: invalid timeOfDay."
    elif timeOfDay == 'N' and demonPresence == 1:
        scene2_status = "Open silently."
    else:
        scene2_status = "Open cautiously."
    result.append(f"[Scene 2] {scene2_status}")

    
    adv = (101 - demonRank * 15) + (swordSharpness * 0.4) + (allyCount * 5)
    strategy = ""
    if adv >= 100:
        strategy = "Engage head-on"
    elif 60 <= adv < 100:
        strategy = "Harass and probe"
    else:
        strategy = "Retreat and regroup"
    result.append(f"[Scene 3] {strategy} (adv = {adv:.1f})")

    
    finalHP = bossHP - totalDamage
    scene4_res = ""
    
    if finalHP <= 0:
        scene4_res = "Boss defeated! (finalHP = 0)"
    elif specialMoveReady == 1 and finalHP <= 50:
        scene4_res = "Use special move to finish!"
    else:
        scene4_res = "Withdraw to heal."
        
    result.append(f"[Scene 4] {scene4_res}")

    return "\n".join(result)




def run_suite():
    


    
    ranges = {
        "slayerLevel": [1, 10],          
        "hp": [10, 200],                 
        "breathing": [0.0, 1.0],         
        "talisman": [0, 1],              
        "time": ['D', 'N', 'X'],         
        "demonPres": [0, 1],             
        "demonRank": [1, 6],             
        "sharpness": [0.0, 100.0],       
        "ally": [0, 10],                 
        "bossHP": [100],                 
        "totalDamage": [40, 60, 110],    
        "special": [0, 1]                
    }

    
    
    test_cases = list(itertools.product(
        ranges["slayerLevel"], ranges["hp"], ranges["breathing"], ranges["talisman"],
        ranges["time"], ranges["demonPres"], ranges["demonRank"], ranges["sharpness"],
        ranges["ally"], ranges["bossHP"], ranges["totalDamage"], ranges["special"]
    ))

    print(f"Bắt đầu chạy {len(test_cases)} testcases...")
    print("-" * 60)

    passed = 0
    failed = 0

    for i, vals in enumerate(test_cases):
        
        (sl, hp, bm, tal, time, dp, dr, sharp, ally, bhp, dmg, spec) = vals

        
        input_str = f"{sl} {hp} {bm} {tal} {time} {dp} {dr} {sharp} {ally} {bhp} {dmg} {spec}"

        
        expected = get_expected_output(sl, hp, bm, tal, time, dp, dr, sharp, ally, bhp, dmg, spec)

        
        try:
            process = subprocess.run(
                [EXECUTABLE_PATH],
                input=input_str,
                text=True,           
                capture_output=True  
            )
            actual = process.stdout.strip() 
            
            
            expected = expected.strip()

            
            if actual == expected:
                passed += 1
            else:
                failed += 1
                print(f"FAILED at Case #{i+1}")
                print(f"Input:\n{input_str}")
                print(f"Expected Output:\n{expected}")
                print(f"Actual Output:\n{actual}")
                
                print("-" * 30)
                break 

        except FileNotFoundError:
            print(f"ERROR: Không tìm thấy file '{EXECUTABLE_PATH}'. Hãy biên dịch C++ trước.")
            return
        except Exception as e:
            print(f"ERROR: Lỗi runtime: {e}")
            return
    print("=" * 60)
    print(f"KẾT QUẢ: {passed} Passed | {failed} Failed")
    if failed == 0:
        print("Chúc mừng! Code của bạn đã vượt qua tất cả các trường hợp biên.")
    else:
        print("Vui lòng sửa code C++ và chạy lại.")

if __name__ == "__main__":
    run_suite()