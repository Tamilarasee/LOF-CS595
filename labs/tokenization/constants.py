TOKEN_PROMPT = """
Extract medical entities, include SNOMED, ICD9, ICD10, LOINC, CPT, and RxNorm codes where applicable. 
Return the response as per the below JSON format 
TOKEN_JSON_FORMAT:
{
    "entities": [
        {
            "text": "Chest pain",
            "begin": 25,
            "end": 30,
            "semantic": "problem",
            "section": "histoy_of_present_illness",
            "assertion": "present",
            "explanation": "Entity found at position 25 to 30 of input text.",
            "codemaps": {
                "icd9cm": {
                    "codes": [
                        {
                            "code": "786.50",
                            "title": "Chest pain, unspecified"
                        }
                    ]
                },
                "icd10cm": {
                    "codes": [
                        {
                            "code": "R07.9",
                            "title": "Chest pain, unspecified"
                        }
                    ]
                },
                "snomed": {
                    "codes": [
                        {
                            "code": "29857009",
                            "title": "Chest pain"
                        }
                    ]
                }
            }
        },
        {
            "text": "Fever",
            "begin": 45,
            "end": 50,
            "semantic": "problem",
            "section": "histoy_of_present_illness",
            "assertion": "present",
            "explanation": "Entity found at position 25 to 30 of input text.",
            "codemaps": {
                "icd9cm": {
                    "codes": [
                        {
                            "code": "087",
                            "title": "Relapsing fever"
                        }
                    ]
                },
                "icd10cm": {
                    "codes": [
                        {
                            "code": "R50.9",
                            "title": "Fever, unspecified"
                        }
                    ]
                },
                "snomed": {
                    "codes": [
                        {
                            "code": "386661006",
                            "title": "Fever"
                        }
                    ]
                }
            }
        },
        {
            "text": "major surgery",
            "begin": 846,
            "end": 859,
            "semantic": "treatment",
            "section": "past_surgical_history",
            "assertion": "absent",
            "explanation": "Entity found at position 846 to 859 of input text.",
            "codemaps": {
                "icd10pcs": {
                    "codes": []
                },
                "loinc": {
                    "codes": []
                },
                "cpt": {
                    "codes": []
                },
                "hcpcs": {
                    "codes": []
                },
                "snomedInternational": {
                    "codes": [
                        {
                            "code": "387713003",
                            "title": "Surgical procedure",
                            "map_type": "Preferred primary",
                            "mesh_code": "D013514"
                        }
                    ]
                }
            }
        },
        {
            "text": "pravastatin",
            "begin": 933,
            "end": 944,
            "type": "standard",
            "semantic": "drug",
            "section": "medications",
            "assertion": "present",
            "explanation": "Entity found at position 933 to 944 of input text.",
            "codemaps": {
                "rxnorm": {
                    "codes": [
                        {
                            "rxnorm_code": "42463",
                            "rxnorm_titles": [
                                {
                                    "title": "pravastatin",
                                    "title_type": "IN"
                                }
                            ]
                        }
                    ]
                },
                "ndc": {
                    "codes": []
                },
                "cvx": {
                    "codes": []
                }
            }
        },
        {
            "text": "respiratory rate",
            "begin": 2165,
            "end": 2181,
            "type": "standard",
            "semantic": "test",
            "section": "physical_examination",
            "assertion": "present",
            "explanation": "Entity found at position 2165 to 2181 of input text.",
            "codemaps": {
                "icd10pcs": {
                    "codes": []
                },
                "loinc": {
                    "codes": [
                        {
                            "code": "9279-1",
                            "title": "Breaths:NRat:Pt:Respiratory system:Qn",
                            "map_type": "Preferred primary"
                        }
                    ]
                },
                "cpt": {
                    "codes": []
                },
                "hcpcs": {
                    "codes": []
                },
                "snomedInternational": {
                    "codes": []
                }
            }
        }
    ]
}
"""