#!/usr/bin/env python3
"""
MATCHUP REPORT GENERATOR V3 - Market-Based Edge Detection

Reads screener_v3 results and generates beautiful HTML report
showing market odds vs model predictions vs Kelly sizing
"""

import pandas as pd
import sys
from datetime import datetime

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    input_file = 'soltar_matchups_with_odds_results_v3.csv'

try:
    df = pd.read_csv(input_file)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matchup Analysis - Market Edge Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header p {{
            font-size: 1.1em;
            opacity: 0.95;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}

        .summary-card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
        }}

        .summary-card .label {{
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .summary-card .value {{
            font-size: 1.8em;
            font-weight: 700;
            color: #667eea;
        }}

        .matchups-container {{
            padding: 40px;
        }}

        .matchup-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 25px;
            transition: all 0.3s ease;
        }}

        .matchup-card:hover {{
            border-color: #667eea;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
        }}

        .matchup-number {{
            position: absolute;
            top: 15px;
            left: 20px;
            background: #667eea;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1em;
        }}

        .matchup-content {{
            margin-left: 0;
        }}

        .players-comparison {{
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            gap: 30px;
            margin-bottom: 30px;
            align-items: start;
        }}

        .player-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .player-name {{
            font-weight: 700;
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #333;
        }}

        .spec-badge {{
            display: inline-block;
            background: #ffc107;
            color: #333;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: 600;
            margin-left: 8px;
        }}

        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
            font-size: 0.95em;
        }}

        .stat-row:last-child {{
            border-bottom: none;
        }}

        .stat-label {{
            color: #6c757d;
            font-weight: 500;
        }}

        .stat-value {{
            font-weight: 700;
            color: #333;
        }}

        .market {{
            color: #999;
        }}

        .model {{
            color: #667eea;
        }}

        .edge {{
            color: #28a745;
            font-weight: 700;
        }}

        .edge.negative {{
            color: #dc3545;
        }}

        .kelly {{
            color: #17a2b8;
            font-weight: 700;
        }}

        .vs {{
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: #6c757d;
            font-size: 1.2em;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 30px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 0.95em;
            border-top: 1px solid #e9ecef;
        }}

        .timestamp {{
            color: #6c757d;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}

            .players-comparison {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}

            .vs {{
                padding: 10px 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Market Edge Analysis</h1>
            <p>Model Predictions vs Market Odds</p>
        </div>

        <div class="summary">
            <div class="summary-card">
                <div class="label">Total Matchups</div>
                <div class="value">{len(df)}</div>
            </div>
            <div class="summary-card">
                <div class="label">Positive Edges</div>
                <div class="value">{len(df[df['matchup_edge'] > 0])}</div>
            </div>
            <div class="summary-card">
                <div class="label">Avg Edge</div>
                <div class="value">{df['matchup_edge'].mean():+.1f}pp</div>
            </div>
            <div class="summary-card">
                <div class="label">Avg Kelly</div>
                <div class="value">{df['kelly_qtr'].mean():.2f}%</div>
            </div>
        </div>

        <div class="matchups-container">
"""

    for idx, row in df.iterrows():
        spec_a = f'<span class="spec-badge">SPEC</span>' if row['spec_a'] == 'YES' else ''
        spec_b = f'<span class="spec-badge">SPEC</span>' if row['spec_b'] == 'YES' else ''

        edge_class = 'edge' if row['matchup_edge'] >= 0 else 'edge negative'

        # Determine bet side and player
        if row['bet_side'] == 'A':
            bet_player = row['player_a']
            bet_spec = row['spec_a'] == 'YES'
        else:
            bet_player = row['player_b']
            bet_spec = row['spec_b'] == 'YES'

        html += f"""
            <div class="matchup-card">
                <div class="matchup-number">{int(row['matchup_num'])}</div>
                <div class="matchup-content">
                    <div class="players-comparison">
                        <div class="player-box">
                            <div class="player-name">{row['player_a']}{spec_a}</div>
                            <div class="stat-row">
                                <span class="stat-label">Market (ML {row['ml_a']}):</span>
                                <span class="stat-value market">{row['implied_a']:.1f}%</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">Our Model:</span>
                                <span class="stat-value model">{row['model_a']:.1f}%</span>
                            </div>
                        </div>
                        <div class="vs">vs</div>
                        <div class="player-box">
                            <div class="player-name">{row['player_b']}{spec_b}</div>
                            <div class="stat-row">
                                <span class="stat-label">Market (ML {row['ml_b']}):</span>
                                <span class="stat-value market">{row['implied_b']:.1f}%</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">Our Model:</span>
                                <span class="stat-value model">{row['model_b']:.1f}%</span>
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e9ecef;">
                        <div class="stat-row">
                            <span class="stat-label">Matchup Edge:</span>
                            <span class="stat-value {edge_class}">{row['matchup_edge']:+.1f}pp (favor {row['bet_side']})</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Quarter Kelly:</span>
                            <span class="stat-value kelly">{row['kelly_qtr']:.2f}% on {bet_player}</span>
                        </div>
                    </div>
                </div>
            </div>
"""

    html += """
        </div>

        <div style="padding: 40px; background: #f8f9fa; border-top: 1px solid #e9ecef;">
            <h2 style="color: #333; margin-bottom: 20px;">Bet Summary & Recommendations</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: #667eea; color: white;">
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">#</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Matchup</th>
                        <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Recommendation</th>
                    </tr>
                </thead>
                <tbody>
"""

    for idx, row in df.iterrows():
        edge = row['matchup_edge']
        kelly = row['kelly_qtr']
        side = row['bet_side']
        player = row['player_a'] if side == 'A' else row['player_b']
        spec = f" [SPEC]" if (row['spec_a'] if side == 'A' else row['spec_b']) else ""

        if kelly < 0.25:
            recommendation = f"<span style='color: #999;'>PASS</span> - Edge too small ({edge:.1f}pp)"
        elif kelly < 0.5:
            recommendation = f"<span style='color: #17a2b8;'>SMALL</span> - {kelly:.2f}% on {player}{spec}"
        elif kelly < 1.0:
            recommendation = f"<span style='color: #667eea;'>MEDIUM</span> - {kelly:.2f}% on {player}{spec}"
        else:
            recommendation = f"<span style='color: #28a745;'>LARGE</span> - {kelly:.2f}% on {player}{spec}"

        html += f"""
                    <tr style="border-bottom: 1px solid #ddd;">
                        <td style="padding: 12px; border: 1px solid #ddd;">#{int(row['matchup_num'])}</td>
                        <td style="padding: 12px; border: 1px solid #ddd;">{row['player_a']} vs {row['player_b']}</td>
                        <td style="padding: 12px; border: 1px solid #ddd;">{recommendation}</td>
                    </tr>
"""

    html += f"""
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p><strong>Market Edge Analysis Report - V3</strong></p>
            <p class="timestamp">Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""

    output_file = input_file.replace('_results_v3.csv', '_report_v3.html')
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"[OK] HTML report generated: {output_file}")
    print()

except FileNotFoundError:
    print(f"[!] File not found: {input_file}")
    sys.exit(1)

except Exception as e:
    print(f"[!] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
