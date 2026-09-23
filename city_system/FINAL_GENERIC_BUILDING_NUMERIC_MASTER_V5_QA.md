# Final Generic Building Numeric Master V5 QA

Generated automatically from repository authority files on the target branch.

## Build result
```text
BUILDING_MASTER_MERGE: PASS rows=104 out=city_system/FINAL_GENERIC_BUILDING_NUMERIC_MASTER_V5.csv
```

## Validation result
```text
Traceback (most recent call last):
  File "/home/runner/work/academic_food_chain/academic_food_chain/city_system/validate_final_building_master_v1.py", line 148, in <module>
    main()
  File "/home/runner/work/academic_food_chain/academic_food_chain/city_system/validate_final_building_master_v1.py", line 137, in main
    result = validate(args.roster, args.roster_v3, args.master, args.tech, args.civic)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/academic_food_chain/academic_food_chain/city_system/validate_final_building_master_v1.py", line 119, in validate
    raise AssertionError("\n".join(errors))
AssertionError: Space Launch Center: tech row Rocketry does not mention building
Nuclear Power Plant: civic row Civil Engineering does not mention building
Recycling Center: civic row Environmentalism does not mention building
Solar Plant: civic row Environmentalism does not mention building
Caravansary: civic row Foreign Trade does not mention building
Mint: civic row Code of Laws does not mention building
Scriptorium: tech row Writing does not mention building
Customs Office: civic row Mercantilism does not mention building
Newspaper Office: tech row Printing does not mention building
Cloth Mill: civic row Guilds does not mention building
Military Academy: civic row Military Training does not mention building
Musicians' Guild: civic row Patronage does not mention building
Opera House: civic row Patronage does not mention building
Navigation School: tech row Cartography does not mention building
Foreign Ministry: CIVIC_GATE not found: Tier-2 government adoption
Grand Master's Chapel: CIVIC_GATE not found: Tier-2 government adoption
Intelligence Agency: CIVIC_GATE not found: Tier-2 government adoption
Shopping Mall: tech row Mass Production does not mention building
Hospital: civic row Urbanization does not mention building
Telegraph Office: civic row Sovereignty does not mention building
Power Plant: civic row Civil Engineering does not mention building
Grid Battery Storage: civic row Global Warming Mitigation does not mention building
Armory: civic row Military Training does not mention building
Garden: tech row Irrigation does not mention building
Airport: civic row Mass Media does not mention building
Radar Station: civic row Mobilization does not mention building
Film Studio: civic row Mass Media does not mention building
Medical Lab: civic row Urbanization does not mention building
National History Museum: CIVIC_GATE not found: Tier-3 government adoption
Royal Society: CIVIC_GATE not found: Tier-3 government adoption
War Department: CIVIC_GATE not found: Tier-3 government adoption
Arsenal: civic row Military Training does not mention building
```

**VERDICT: FAIL - inspect validation output above before treating the merged master as authoritative.**
