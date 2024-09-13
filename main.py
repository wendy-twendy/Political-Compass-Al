# ... (previous code remains unchanged)

def get_quadrant_explanation(economic_score, libertarian_authoritarian_score):
    quadrant = ""
    explanation = ""
    
    # Determine the intensity of the position
    economic_intensity = abs(economic_score)
    social_intensity = abs(libertarian_authoritarian_score)
    
    if economic_intensity < 3 and social_intensity < 3:
        quadrant = "Centrist"
        explanation = (
            "You hold moderate views on both economic and social issues. Centrists often seek balanced approaches "
            "to political problems, drawing ideas from both left and right. You may support a mixed economy with "
            "elements of both free market and government intervention, and moderate policies on social issues. "
            "Centrists often prioritize pragmatism and compromise over ideological purity."
        )
    elif economic_score < 0 and libertarian_authoritarian_score > 0:
        quadrant = "Authoritarian Left"
        explanation = (
            "Your views align with the Authoritarian Left quadrant. This position combines left-wing economic "
            "policies with authoritarian social policies. You likely support significant government intervention "
            "in the economy, including wealth redistribution and strong welfare programs. On social issues, you "
            "may favor a strong state that can enforce collective goals and maintain social order. Historical "
            "examples include certain forms of socialism and communism."
        )
    elif economic_score >= 0 and libertarian_authoritarian_score > 0:
        quadrant = "Authoritarian Right"
        explanation = (
            "Your views align with the Authoritarian Right quadrant. This position combines right-wing economic "
            "policies with authoritarian social policies. You likely support free market capitalism with some state "
            "intervention to maintain order and tradition. On social issues, you may favor a strong government that "
            "enforces conservative values and national interests. Historical examples include certain forms of "
            "nationalism and traditionalist conservatism."
        )
    elif economic_score < 0 and libertarian_authoritarian_score <= 0:
        quadrant = "Libertarian Left"
        explanation = (
            "Your views align with the Libertarian Left quadrant. This position combines left-wing economic policies "
            "with libertarian social policies. You likely support collective ownership or significant wealth "
            "redistribution, but with minimal state intervention in personal matters. You may advocate for worker-controlled "
            "enterprises, strong civil liberties, and decentralized decision-making. This aligns with ideologies like "
            "anarcho-communism or libertarian socialism."
        )
    else:  # economic_score >= 0 and libertarian_authoritarian_score <= 0
        quadrant = "Libertarian Right"
        explanation = (
            "Your views align with the Libertarian Right quadrant. This position combines right-wing economic policies "
            "with libertarian social policies. You likely support free market capitalism with minimal government "
            "intervention in both economic and social spheres. You may advocate for lower taxes, deregulation, and "
            "maximum individual liberty in personal matters. This aligns with ideologies like classical liberalism "
            "or anarcho-capitalism."
        )
    
    # Add intensity to the explanation
    if economic_intensity > 7 or social_intensity > 7:
        explanation += " Your position is quite extreme on one or both axes, indicating strong convictions in your political beliefs."
    elif economic_intensity > 3 or social_intensity > 3:
        explanation += " Your position is moderately strong, indicating clear preferences in your political views."
    else:
        explanation += " Your position is relatively close to the center, indicating more moderate views."
    
    return quadrant, explanation

# ... (rest of the code remains unchanged)
