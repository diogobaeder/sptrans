LINE_SEARCH = b"""
[
    {
        "CodigoLinha": 1273,
        "Circular": false,
        "Letreiro": "8000",
        "Sentido": 1,
        "Tipo": 10,
        "DenominacaoTPTS": "PCA.RAMOS DE AZEVEDO",
        "DenominacaoTSTP": "TERMINAL LAPA",
        "Informacoes": null
    },
    {
        "CodigoLinha": 34041,
        "Circular": false,
        "Letreiro": "8000",
        "Sentido": 2,
        "Tipo": 10,
        "DenominacaoTPTS": "PCA.RAMOS DE AZEVEDO",
        "DenominacaoTSTP": "TERMINAL LAPA",
        "Informacoes": null
    }
]
"""

STOP_SEARCH = b"""
[
  {
    "CodigoParada": 340015329,
    "Nome": "AFONSO BRAZ B/C1",
    "Endereco": "R ARMINDA/ R BALTHAZAR DA VEIGA",
    "Latitude": -23.592938,
    "Longitude": -46.672727
  },
  {
    "CodigoParada": 340015328,
    "Nome": "AFONSO BRAZ B/C2",
    "Endereco": "R ARMINDA/ R BALTHAZAR DA VEIGA",
    "Latitude": -23.59337,
    "Longitude": -46.672766
  },
  {
    "CodigoParada": 340015333,
    "Nome": "AFONSO BRAZ C/B1",
    "Endereco": "R DOUTORA MARIA AUGUSTA SARAIVA/ R NATIVIDADE",
    "Latitude": -23.596028,
    "Longitude": -46.673378
  },
  {
    "CodigoParada": 340015331,
    "Nome": "AFONSO BRAZ C/B2",
    "Endereco": "R DOUTORA MARIA AUGUSTA SARAIVA/ R NATIVIDADE",
    "Latitude": -23.595374,
    "Longitude": -46.673207
  }
]
"""

STOP_SEARCH_BY_LINE = b"""
[
  {
    "CodigoParada": 7014417,
    "Nome": "ANGELICA B/C",
    "Endereco": "AV   ANGELICA",
    "Latitude": -23.534587,
    "Longitude": -46.654178
  },
  {
    "CodigoParada": 60016784,
    "Nome": "PALMEIRAS B/C",
    "Endereco": " R PADRE ANTONIO TOMAS/ AV POMPEIA ",
    "Latitude": -23.525834,
    "Longitude": -46.679254
  }
]
"""

STOP_SEARCH_BY_LANE = b"""
[
  {
    "CodigoParada": 260016859,
    "Nome": "ANTONIA DE QUEIROS B/C",
    "Endereco": " R DONA ANTONIA DE QUEIROS/ R PIAUI ",
    "Latitude": -23.549577,
    "Longitude": -46.653216
  },
  {
    "CodigoParada": 260016858,
    "Nome": "ANTONIA DE QUEIROS C/B",
    "Endereco": " R DONA ANTONIA DE QUEIROS/ R PIAUI ",
    "Latitude": -23.54958,
    "Longitude": -46.65343
  }
]
"""

LANES = b"""
[
  {
    "CodCorredor": 8,
    "CodCot": 0,
    "Nome": "Campo Limpo"
  }
]
"""

VEHICLE_POSITIONS = b"""
{
  "hr": "22:57",
  "vs": [
    {
      "p": "11433",
      "a": false,
      "py": -23.540150375000003,
      "px": -46.64414075
    },
    {
      "p": "12132",
      "a": false,
      "py": -23.5200315,
      "px": -46.699387
    }
  ]
}
"""

FORECAST_FOR_LINE_AND_STOP = b"""
{
  "hr": "23:09",
  "p": {
    "cp": 4200953,
    "np": "PARADA ROBERTO SELMI DEI B/C",
    "py": -23.675901,
    "px": -46.752812,
    "l": [
      {
        "c": "7021-10",
        "cl": 1989,
        "sl": 1,
        "lt0": "TERM. JOÃO DIAS",
        "lt1": "JD. MARACÁ",
        "qv": 1,
        "vs": [
          {
            "p": "74558",
            "t": "23:11",
            "a": true,
            "py": -23.67603,
            "px": -46.75891166666667
          }
        ]
      }
    ]
  }
}
"""

FORECAST_FOR_LINE = b"""
{
  "hr": "23:18",
  "ps": [
    {
      "cp": 700016623,
      "np": "ANA CINTRA B/C",
      "py": -23.538763,
      "px": -46.646925,
      "vs": [
        {
          "p": "11436",
          "t": "23:26",
          "a": false,
          "py": -23.528119999999998,
          "px": -46.670674999999996
        }
      ]
    },
    {
      "cp": 7014417,
      "np": "ANGELICA B/C",
      "py": -23.534587,
      "px": -46.654178,
      "vs": [
        {
          "p": "11436",
          "t": "23:23",
          "a": false,
          "py": -23.528119999999998,
          "px": -46.670674999999996
        }
      ]
    }
  ]
}
"""

FORECAST_FOR_STOP = b"""
{
  "hr": "23:20",
  "p": {
    "cp": 4200953,
    "np": "PARADA ROBERTO SELMI DEI B/C",
    "py": -23.675901,
    "px": -46.752812,
    "l": [
      {
        "c": "675K-10",
        "cl": 198,
        "sl": 1,
        "lt0": "METRO STA CRUZ",
        "lt1": "TERM. JD. ANGELA",
        "qv": 2,
        "vs": [
          {
            "p": "73651",
            "t": "23:22",
            "a": true,
            "py": -23.676623333333335,
            "px": -46.757641666666665
          },
          {
            "p": "73816",
            "t": "23:24",
            "a": true,
            "py": -23.681900000000002,
            "px": -46.76727833333333
          }
        ]
      },
      {
        "c": "737A-10",
        "cl": 1730,
        "sl": 1,
        "lt0": "TERM  STO AMARO",
        "lt1": "TERM JD ÂNGELA",
        "qv": 1,
        "vs": [
          {
            "p": "72089",
            "t": "23:22",
            "a": true,
            "py": -23.677310000000002,
            "px": -46.761109999999995
          }
        ]
      }
    ]
  }
}
"""
