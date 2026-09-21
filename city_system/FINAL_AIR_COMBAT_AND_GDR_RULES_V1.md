# Final Air Combat and GDR Module Rules V1

Date: 2026-09-21
Status: **LOCKED V1**

## GDR Future modules

Gathering Storm values are retained directly where they map cleanly onto the project's Civ V-scale GDR.

Base project GDR:
- Combat 150
- Ranged Combat 100
- Range 3
- Moves 5
- Production 550
- Uranium slot 1
- ordinary promotion profile: NONE

Advanced AI:
- Drone Air Defense
- Anti-Air Defense Strength 130
- project interception chance 100%
- interception radius 2

Advanced Power Cells:
- Particle Beam Siege Cannon
- city/defense ranged strength: 100 -> 130
- 100% effectiveness against city defenses

Cybernetics:
- Enhanced Mobility
- Moves 5 -> 8
- Mountain Jump action

Smart Materials:
- Reinforced Armor Plating
- +10 Combat Strength when defending against land/naval attacks

Base Gathering Storm identity retained:
- no ordinary XP/promotions
- may move/fight on Coast/Ocean without ordinary embarkation
- heals only in friendly territory

## Civ V-style air interception

Interception chance:
- Triplane: 50%
- Fighter: 100%
- Jet Fighter: 100%
- Anti-Air Gun: 100%
- Mobile SAM: 100%
- Destroyer: 40%
- Missile Cruiser: 100%

GDR is conditional:
- no interception before Advanced AI
- after Advanced AI: 100% project-adapted interception with AA Strength 130

## Interception sequence

For each hostile air attack entering interception coverage:

1. Roll evasion.
2. If evasion succeeds, no interception occurs.
3. Otherwise choose one available interceptor covering the target.
4. Roll that unit's interception chance.
5. If successful, resolve interception damage.
6. The air strike continues if the attacker survives.

Only one interceptor may resolve a given air attack.

Base interception capacity:
- 1 per interceptor per turn
- Sortie promotion: fighter gets +1 interception

Interception is an extra defensive action and does not consume the interceptor's normal movement/action.

## Evasion

Innate:
- Stealth Bomber: 100%
- Guided Missile: 100%

These cannot be intercepted under the baseline V1 system.

Earned bomber promotion:
- Evasion reduces interception damage by 50%
- it does not change evasion chance to 50%

This distinction follows the Civ V data model.

## Air Sweep

Eligible:
- Triplane
- Fighter
- Jet Fighter

Effect:
- triggers an enemy interceptor intentionally;
- consumes one interception from that defender;
- fighter-vs-fighter resolves as air-to-air dogfight;
- ground/naval interceptor damage against the sweeping fighter uses Civ V's reduced-damage sweep treatment.

V1 intentionally does not assign an unsupported exact reduction percentage to surface-interceptor sweep damage.

## Fighter identity

Triplane / Fighter / Jet Fighter:
- Air Sweep
- Air Recon radius 6
- +150% vs bomber and helicopter targets
- normal air strike against land/naval target: -50% ranged strength

This prevents fighters from replacing bombers as generic strike aircraft.

## Ground AA

Anti-Air Gun and Mobile SAM:
- interception radius 2
- interception chance 100%
- +150% vs aircraft and helicopters

## Naval AA

Destroyer:
- interception chance 40%
- radius 2
- one interception/turn

Missile Cruiser:
- interception chance 100%
- radius 2
- one interception/turn

Their anti-submarine abilities remain separate innate rules.

## Source basis

Civ V air combat:
- evasion is tested before interception;
- one interceptor per air strike;
- interceptors normally intercept once per turn;
- Air Sweep consumes interception capability.

Civ V unit attributes:
- Triplane Interception 50
- Fighter / Jet Fighter Interception 100
- AA Gun / Mobile SAM Interception 100
- Destroyer Interception 40
- Missile Cruiser Interception 100
- Stealth Bomber Evasion 100
- Guided Missile Evasion 100

Gathering Storm GDR:
- Drone Air Defense 130
- Particle Beam Siege Cannon +30 ranged vs city/encampment and full effectiveness
- Enhanced Mobility +3 Moves + Mountain Jump
- Reinforced Armor +10 defense vs land/naval
