def mbti(q1: str, q2: str, q3: str, q4: str, q5: str, q6: str, q7: str, q8: str, q9: str,q10:str) -> str:
    
    prompt = f"""
        Question 1: Do you prefer to focus on the outer world or your own inner world? 
        Answer: {q1},
        Question 2: How do you prefer to take in information? Please provide your comment. 
        Answer: {q2},
        Question 3: How do you make decisions? Please provide your comment. 
        Answer: {q3},
        Question 4: Do you prefer a structured and organized lifestyle or a flexible and spontaneous one? Please provide your comment.
        Answer: {q4},
        Question 5: How do you approach and interact with others? Please provide your comment.
        Answer: {q5},
        Question 6: Are you more inclined to follow your head or your heart? Please provide your comment.
        Answer: {q6},
        Question 7: Do you prefer to plan ahead or be open to new possibilities? Please provide your comment.
        Answer: {q7},
        Question 8: How do you handle and process emotions? Please provide your comment.
        Answer: {q8},
        Question 9: Are you more inclined to be assertive or accommodating? Please provide your comment.Answer: {q9},
        Question 10: How do you recharge and regain energy? Please provide your comment. 
        Answer: {q10}
        """
    
    return prompt

def astrology(name: str, gender: str, dob: str, tob: str, pob: str,
                     father_name: str, mother_name: str, nationality: str,
                     birth_weight: float, birth_length: float, birth_order: int,
                     siblings: int, education: str, profession: str, marital_status: str,
                     spouse_name: str, children: int, current_location: str,
                     moon_degree: float, moon_sign: str, moon_nakshatra: str) -> str:
    
    prompt: str = f"""I want you to think of yourself as a Vedic Astrologer, and take in the following list of inputs to predict the Nakshatra and Rashi of the individual. 

        Name: {name}
        Gender: {gender}
        Date of Birth: {dob}
        Time of Birth: {tob}
        Place of Birth: {pob}
        Father's Name: {father_name}
        Mother's Name: {mother_name}
        Nationality: {nationality}
        Birth Weight: {birth_weight} kg
        Birth Length: {birth_length} cm
        Birth Order: {birth_order}
        Siblings: {siblings}
        Education: {education}
        Profession: {profession}
        Marital Status: {marital_status}
        Spouse's Name: {spouse_name}
        Number of Children: {children}
        Current Location: {current_location}
        Moon's Degree: {moon_degree}
        Moon's Sign: {moon_sign}
        Moon's Nakshatra: {moon_nakshatra}

    """

    return prompt

"""
Vedic astrology is a voodoo trick. What it does correctly is that it has been designed by observing the Indian populace and dividing it into 27 nakshatras. The 12 rashis are an additional layer. And next, this observation is mapped against the movement of planets to trick people to believe that there's a correlation between movement of planets and stars with your destiny. While it might be correct to a certain extent, a lot of that is bogus.
"""
