import plotly.graph_objects as go

def generate_plot(economic_score, libertarian_authoritarian_score):
    fig = go.Figure()

    # Add quadrants with updated colors
    quadrants = [{
        "name": "Authoritarian Left",
        "x": [-10, 0, 0, -10],
        "y": [0, 0, 10, 10],
        "color": "#ff7575"
    }, {
        "name": "Authoritarian Right",
        "x": [0, 10, 10, 0],
        "y": [0, 0, 10, 10],
        "color": "#42aaff"
    }, {
        "name": "Libertarian Left",
        "x": [-10, 0, 0, -10],
        "y": [0, 0, -10, -10],
        "color": "#9aed97"
    }, {
        "name": "Libertarian Right",
        "x": [0, 10, 10, 0],
        "y": [0, 0, -10, -10],
        "color": "#c09aec"
    }]

    for quadrant in quadrants:
        fig.add_trace(
            go.Scatter(x=quadrant["x"],
                       y=quadrant["y"],
                       fill="toself",
                       fillcolor=quadrant["color"],
                       line=dict(color="rgba(0,0,0,0)"),
                       showlegend=False,
                       hoverinfo="skip"))

    # Update grid lines to stay within [-10, 10] range
    for i in range(-4, 5):
        fig.add_shape(type="line",
                      x0=-10,
                      x1=10,
                      y0=i * 2.5,
                      y1=i * 2.5,
                      line=dict(color="rgba(255,255,255,0.8)", width=1))
        fig.add_shape(type="line",
                      x0=i * 2.5,
                      x1=i * 2.5,
                      y0=-10,
                      y1=10,
                      line=dict(color="rgba(255,255,255,0.8)", width=1))

    # Add black center lines
    fig.add_shape(type="line",
                  x0=0,
                  x1=0,
                  y0=-10,
                  y1=10,
                  line=dict(color="black", width=2))
    fig.add_shape(type="line",
                  x0=-10,
                  x1=10,
                  y0=0,
                  y1=0,
                  line=dict(color="black", width=2))

    # Update layout with exact [-10, 10] plot range
    fig.update_layout(xaxis=dict(range=[-10, 10],
                                 zeroline=False,
                                 showticklabels=False),
                      yaxis=dict(range=[-10, 10],
                                 zeroline=False,
                                 showticklabels=False),
                      showlegend=False,
                      width=700,
                      height=700,
                      margin=dict(l=80, r=80, t=80, b=80),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)")

    # Add axis labels with adjusted positions, font size, and weight
    fig.add_annotation(x=-10,
                       y=0,
                       text="Left",
                       showarrow=False,
                       xanchor="right",
                       yanchor="middle",
                       xref="x",
                       yref="y",
                       font=dict(size=16, weight=900, color="black"))
    fig.add_annotation(x=10,
                       y=0,
                       text="Right",
                       showarrow=False,
                       xanchor="left",
                       yanchor="middle",
                       xref="x",
                       yref="y",
                       font=dict(size=16, weight=900, color="black"))
    fig.add_annotation(x=0,
                       y=10,
                       text="Authoritarian",
                       showarrow=False,
                       xanchor="center",
                       yanchor="bottom",
                       xref="x",
                       yref="y",
                       font=dict(size=16, weight=900, color="black"))
    fig.add_annotation(x=0,
                       y=-10,
                       text="Libertarian",
                       showarrow=False,
                       xanchor="center",
                       yanchor="top",
                       xref="x",
                       yref="y",
                       font=dict(size=16, weight=900, color="black"))

    # Add user's position as the last element
    fig.add_trace(
        go.Scatter(x=[economic_score],
                   y=[libertarian_authoritarian_score],
                   mode="markers+text",
                   marker=dict(color="red", size=12, symbol="square"),
                   text=["You"],
                   textposition="top center",
                   textfont=dict(size=12, color="black")))

    return fig.to_json()

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
            "elements of both free market and government intervention, and moderate policies on social issues."
        )
    elif economic_score < 0 and libertarian_authoritarian_score > 0:
        quadrant = "Authoritarian Left"
        if economic_intensity > 7 and social_intensity > 7:
            explanation = (
                "You hold strong authoritarian left views, combining left-wing economic policies with highly "
                "authoritarian social policies. You likely support extensive government control over the economy, "
                "significant wealth redistribution, and strong state intervention in social issues. Historical "
                "examples include Stalinist communism and other forms of totalitarian socialism."
            )
        elif economic_intensity > 3 or social_intensity > 3:
            explanation = (
                "You lean towards authoritarian left views, favoring significant government involvement in both "
                "economic and social spheres. You may support a planned economy, extensive welfare programs, and "
                "believe that individual freedoms should sometimes be sacrificed for the collective good. This "
                "position is similar to some forms of democratic socialism or left-wing populism."
            )
        else:
            explanation = (
                "You have slight authoritarian left tendencies, combining moderate left-leaning economic views "
                "with a preference for some government control over social issues. You might support a mixed "
                "economy with strong regulations and some wealth redistribution, while also favoring some "
                "restrictions on personal freedoms for societal benefit.")
    elif economic_score >= 0 and libertarian_authoritarian_score > 0:
        quadrant = "Authoritarian Right"
        if economic_intensity > 7 and social_intensity > 7:
            explanation = (
                "You hold strong authoritarian right views, combining right-wing economic policies with highly "
                "authoritarian social policies. You likely support free market capitalism with some state "
                "intervention to maintain order, strong national defense, and traditional social values enforced "
                "by the state. Historical examples include fascist regimes and some military dictatorships."
            )
        elif economic_intensity > 3 or social_intensity > 3:
            explanation = (
                "You lean towards authoritarian right views, favoring free market principles with some government "
                "involvement and conservative social policies. You may support a strong state to enforce law and "
                "order, traditional values, and national interests. This position is similar to some forms of "
                "conservative nationalism or right-wing populism.")
        else:
            explanation = (
                "You have slight authoritarian right tendencies, combining moderate right-leaning economic views "
                "with a preference for some government control over social issues. You might support a largely "
                "free market with some regulations, while also favoring some restrictions on personal freedoms "
                "to maintain social order and traditional values.")
    elif economic_score < 0 and libertarian_authoritarian_score <= 0:
        quadrant = "Libertarian Left"
        if economic_intensity > 7 and social_intensity > 7:
            explanation = (
                "You hold strong libertarian left views, combining left-wing economic policies with highly "
                "libertarian social policies. You likely support collective ownership, worker-controlled "
                "enterprises, and maximum personal and social freedom. This position is similar to anarcho-communism "
                "or libertarian socialism.")
        elif economic_intensity > 3 or social_intensity > 3:
            explanation = (
                "You lean towards libertarian left views, favoring significant economic equality and social freedom. "
                "You may support decentralized economic planning, strong civil liberties, and community-based "
                "decision making. This position is similar to some forms of democratic socialism or left-libertarianism."
            )
        else:
            explanation = (
                "You have slight libertarian left tendencies, combining moderate left-leaning economic views with "
                "a preference for personal and social freedoms. You might support a mixed economy with significant "
                "public services and wealth redistribution, while also advocating for civil liberties and social "
                "progressivism.")
    else:  # economic_score >= 0 and libertarian_authoritarian_score <= 0
        quadrant = "Libertarian Right"
        if economic_intensity > 7 and social_intensity > 7:
            explanation = (
                "You hold strong libertarian right views, combining right-wing economic policies with highly "
                "libertarian social policies. You likely support laissez-faire capitalism, minimal government "
                "intervention in both economic and social spheres, and maximum individual liberty. This position "
                "is similar to anarcho-capitalism or extreme forms of classical liberalism."
            )
        elif economic_intensity > 3 or social_intensity > 3:
            explanation = (
                "You lean towards libertarian right views, favoring free market principles and significant personal "
                "freedoms. You may support minimal government regulation of the economy, low taxes, and a non-interventionist "
                "foreign policy, while also advocating for civil liberties and social freedoms. This position is "
                "similar to minarchism or some forms of classical liberalism.")
        else:
            explanation = (
                "You have slight libertarian right tendencies, combining moderate right-leaning economic views "
                "with a preference for personal and social freedoms. You might support a largely free market with "
                "minimal government intervention, while also advocating for civil liberties and a live-and-let-live "
                "approach to social issues.")

    # Handle cases where one axis is centrist but the other is not
    if economic_intensity < 3 and social_intensity >= 3:
        if libertarian_authoritarian_score > 0:
            quadrant = "Centrist Authoritarian"
            explanation = (
                "You hold centrist views on economic issues but lean authoritarian on social issues. You may support "
                "a mixed economy with balanced government intervention, but believe in stronger state control over "
                "social and personal matters. This could manifest as support for technocracy or certain forms of "
                "state capitalism combined with socially conservative policies."
            )
        else:
            quadrant = "Centrist Libertarian"
            explanation = (
                "You hold centrist views on economic issues but lean libertarian on social issues. You may support "
                "a mixed economy with balanced government intervention, while strongly advocating for personal freedoms "
                "and civil liberties. This position often emphasizes pragmatic economic policies combined with progressive "
                "social values and a limited government approach to personal matters."
            )
    elif social_intensity < 3 and economic_intensity >= 3:
        if economic_score < 0:
            quadrant = "Left-Leaning Centrist"
            explanation = (
                "You hold left-leaning views on economic issues but centrist views on social issues. You may support "
                "significant government intervention in the economy, wealth redistribution, and strong public services, "
                "while taking a more moderate stance on social and cultural issues. This position often seeks to balance "
                "economic progressivism with pragmatic approaches to social policy."
            )
        else:
            quadrant = "Right-Leaning Centrist"
            explanation = (
                "You hold right-leaning views on economic issues but centrist views on social issues. You may support "
                "free market principles, lower taxes, and limited government intervention in the economy, while taking "
                "a more moderate stance on social and cultural issues. This position often seeks to balance economic "
                "conservatism with pragmatic approaches to social policy.")

    return quadrant, explanation
