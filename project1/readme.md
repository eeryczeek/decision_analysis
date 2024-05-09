`Eryk Ptaszyński 151950`, `Eryk Walter 151931`

# 3.1:

| Question                                                                                                                                                                                                                                                                                                                                                        | Answer                                                                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| What is the domain of the problem about?                                                                                                                                                                                                                                                                                                                        | The domain of the problem is about economic indicators of different countries.                                                                                                                                          |
| What is the source of the data?                                                                                                                                                                                                                                                                                                                                 | [github](https://github.com/Valdecy/Datasets/blob/master/MCDA/MCDA-01-ECI%202019.txt)                                                                                                                                   |
| What is the point of view of the decision maker?                                                                                                                                                                                                                                                                                                                | The point of view of the decision maker is not specified in the question.                                                                                                                                               |
| What is the number of alternatives considered? Were there more of them in the original data set?                                                                                                                                                                                                                                                                | The number of alternatives considered is equal to the number of countries in the dataset (**36**). There were more in the original dataset.                                                                             |
| Describe one of the alternatives considered (give its name, evaluations, specify preferences for this alternative)                                                                                                                                                                                                                                              | One of the alternatives considered is Angola: (Gross Domestic Product: 198.8652, Unemployment Rate: 0.136317784, Income Tax Rate: 18.6, Inflation: 0.040629596, Total Reserves: 17330953410.0, GINI: 51.3)              |
| What is the number of criteria considered? Were there more of them in the original data set?                                                                                                                                                                                                                                                                    | The number of criteria considered is six (Gross Domestic Product, Unemployment Rate, Income Tax Rate, Inflation, Total Reserves, GINI). There were more in the original dataset.                                        |
| What is the origin of the various criteria? (catalog parameter / created by the decision maker - how?)                                                                                                                                                                                                                                                          | These criteria are financial and economic indicators                                                                                                                                                                    |
| What are the domains of the individual criteria (discrete / continuous)? Note: in the case of continuous domains, specify the range of the criterion’s variability, in the case of others: list the values. What is the nature (gain / cost) of the individual criteria?                                                                                        | All criterions are continuous type. `Unemployment Rate` and `Inflation` are in range [0, 1], `Income Tax Rate` and `GINI` are in range [0, 100] and finally `Gross Domestic Product` and `Total Reserves` are unbounded |
| Are all criteria of equal importance (should they have the same ”weights”)? If not, can the relative importance of the criteria under consideration be expressed in terms of weights? In this case, estimate the weights of each criterion on a scale of 1 to 10. Are there any criteria among the criteria that are completely or almost invalid / irrelevant? | "Gross Domestic Product": "weight": 3, "Unemployment Rate": "weight": 9, "Income Tax Rate": "weight": 1, "Inflation": "weight": 5, "Total Reserves": "weight": 7, "GINI": "weight": 3                                   |
| What should the theoretically best alternative look like in your opinion? Is it a small advantage on many criteria, or rather a strong advantage on few (but key) criteria? Which?                                                                                                                                                                              | rather a small advantage on many criteria                                                                                                                                                                               |
| Which of the considered alternatives (provide name and values on individual criteria) seems to be the best / definitely better than the others? Is it determined by one reason (e.g. definitely the lowest price) or rather the overall value of the criteria? Does this alternative still have any weaknesses?                                                 | Indonesia - it has good overall stats: high GDP, desired unemployment rate, and really low inflation                                                                                                                    |
| Which of the considered alternatives (provide name and values on individual criteria) seems to be the worst / definitely worse than the others? Is it determined by one reason (e.g. definitely the highest price), or rather the overall value of the criteria? Does this alternative still have any strengths?                                                | Uganda - extremely high unemployment rate                                                                                                                                                                               |

# 3.2

Write the preferential information you provided at the input of the method:

```python
parameters = {
    "Gross Domestic Product": {"type": "gain", "q": 100, "p": 1000, "weight": 1},
    "Unemployment Rate": {"type": "cost", "q": 0.1, "p": 0.2, "weight": 1},
    "Income Tax Rate": {"type": "cost", "q": 1, "p": 1, "weight": 1},
    "Inflation": {"type": "cost", "q": 0, "p": 0.1, "weight": 1},
    "Total Reserves": {"type": "gain", "q": 1, "p": 1000, "weight": 1},
    "GINI": {"type": "cost", "q": 1, "p": 1, "weight": 1},
}
```

## Promethee1 and Promethee2 results:

![promethee1](./results/ranking_graph_promethee1.png)

![promethee2](./results/ranking_graph_promethee2.png)

promethee2 ranking in the form of pd.Series:

```
Indonesia 17.860558
Turkey 17.135487
India 15.351422
Brazil 14.364812
Ukraine 12.466943
Argentina 12.166046
Mexico 8.496966
Spain 8.026358
Hungary 7.471940
South Africa 6.472234
Romania 6.228796
Angola 5.183187
Tunisia 4.665039
Colombia 4.477009
Philippines 1.794077
Belarus 0.133006
Chile -0.439259
Moldova -1.113362
Serbia -1.583181
Peru -1.648398
Ethiopia -1.955974
Greece -2.196546
Georgia -2.888979
Mozambique -2.891422
Mongolia -3.004487
Portugal -3.692172
Guatemala -4.197193
Paraguay -4.904149
Madagascar -5.905541
Honduras -6.382364
Thailand -7.688341
Costa Rica -8.236588
Armenia -8.343137
Namibia -8.826039
Slovenia -10.206500
El Salvador -11.059238
Panama -12.475220
Tanzania -14.469100
Uganda -18.186692
```

Indonesia is indeed the best country in the whole world. Its economic indicators prove that it is second to none and we should all live there. On the other hand, Uganda, even though popular a few years ago because of the "Ugandan Knucles" memes, does not offer its inhabitants any prospects for a fantastic future.

# 3.3 Problem analysis with the use of ELECTRE TRI-B

```
             Class
Angola          C1
Argentina       C1
Armenia         C1
Belarus         C1
Brazil          C3
Chile           C1
Colombia        C1
Costa Rica      C1
El Salvador     C1
Ethiopia        C1
Georgia         C2
Greece          C1
Guatemala       C1
Honduras        C1
Hungary         C3
India           C3
Indonesia       C2
Madagascar      C1
Mexico          C2
Moldova         C1
Mongolia        C1
Mozambique      C1
Namibia         C1
Panama          C1
Paraguay        C1
Peru            C1
Philippines     C1
Portugal        C1
Romania         C1
Serbia          C1
Slovenia        C1
South Africa    C1
Spain           C1
Tanzania        C1
Thailand        C1
Tunisia         C1
Turkey          C2
Uganda          C1
Ukraine         C1
```

We thought that Indonesia, which we had previously described as the best place in the world, would beat all other alternatives.
