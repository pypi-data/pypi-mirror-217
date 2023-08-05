import pandas as pd
from collections import defaultdict
from a_pandas_ex_less_memory_more_speed import pd_add_less_memory_more_speed

pd_add_less_memory_more_speed()
from dict_merger_keep_all import dict_merger
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()
nested_di = lambda: defaultdict(nested_di)

dtypes = {
    "dep": "string",
    "doc": "object",
    "ent_id": "category",
    "ent_iob": "string",
    "ent_kb_id": "category",
    "ent_type": "string",
    "has_vector": "bool",
    "head": "object",
    "is_alpha": "bool",
    "is_ascii": "bool",
    "is_bracket": "bool",
    "is_currency": "bool",
    "is_digit": "bool",
    "is_left_punct": "bool",
    "is_lower": "bool",
    "is_oov": "bool",
    "is_punct": "bool",
    "is_quote": "bool",
    "is_right_punct": "bool",
    "is_sent_end": "bool",
    "is_sent_start": "bool",
    "is_space": "bool",
    "is_stop": "bool",
    "is_title": "bool",
    "is_upper": "bool",
    "lang": "category",
    "left_edge": "object",
    "lemma": "string",
    "like_email": "bool",
    "like_num": "bool",
    "like_url": "bool",
    "lower": "string",
    "n_lefts": "uint8",
    "n_rights": "bool",
    "morph": "object",
    "norm": "string",
    "orth": "string",
    "pos": "string",
    "prefix": "string",
    "rank": "uint64",
    "right_edge": "object",
    "sent": "object",
    "sent_start": "object",
    "sentiment": "Float64",
    "shape": "string",
    "suffix": "string",
    "tag": "string",
    "ancestors": "object",
    "children": "object",
    "lefts": "object",
    "rights": "object",
    "subtree": "object",
    "iob_strings": "object",
}


def spacy2df(doc, colprefix: str = "") -> pd.DataFrame:
    r"""
        Convert a Spacy `doc` object into a pandas DataFrame.

        Parameters:
            doc (spacy.tokens.doc.Doc): The Spacy `doc` object to convert.
            colprefix (str, optional): Prefix for column names in the DataFrame. Defaults to an empty string.

        Returns:
            pd.DataFrame: The resulting DataFrame containing the attributes of the Spacy `doc` object.

        Example:
            import spacy
            import pandas as pd
            from spacy2df import spacy2df

            # Load Spacy model and create a doc object
            nlp = spacy.load("pt_core_news_sm")
            frase = "Rede do Banco Itaú é bom"
            doc = nlp(frase)

            # Convert the doc object to a DataFrame
            df = spacy2df(doc, colprefix='aa_')
            print(df)

                  aa_dep                    aa_doc aa_ent_id aa_ent_iob aa_ent_kb_id aa_ent_type  aa_has_vector aa_head  aa_is_alpha  aa_is_ascii  aa_is_bracket  aa_is_currency  aa_is_digit  aa_is_left_punct  aa_is_lower  aa_is_oov  aa_is_punct  aa_is_quote  aa_is_right_punct  aa_is_sent_end  aa_is_sent_start  aa_is_space  aa_is_stop  aa_is_title  aa_is_upper aa_lang aa_left_edge aa_lemma  aa_like_email  aa_like_num  aa_like_url aa_lower  aa_n_lefts  aa_n_rights                                                                              aa_morph aa_norm aa_orth aa_pos aa_prefix               aa_rank aa_right_edge                          aa_sent aa_sent_start  aa_sentiment aa_shape aa_suffix aa_tag        aa_ancestors aa_children   aa_lefts aa_rights                       aa_subtree aa_iob_strings morph_Gender morph_Number morph_Definite morph_PronType morph_Mood  morph_Person morph_Tense morph_VerbForm
    0      nsubj  Rede do Banco Itaú é bom                    O                                    True     bom         True         True          False           False        False             False        False       True        False        False              False           False              True        False       False         True        False      pt         Rede     rede          False        False        False     rede           0         True                                                   {'Gender': 'Fem', 'Number': 'Sing'}    rede    Rede  PROPN         R  18446744073709551615          Itaú  (Rede, do, Banco, Itaú, é, bom)         False           0.0     Xxxx       ede  PROPN              (bom,)    (Banco,)         ()  (Banco,)          (Rede, do, Banco, Itaú)    (, I, O, B)          Fem         Sing           <NA>           <NA>       <NA>          <NA>        <NA>           <NA>
    1       case  Rede do Banco Itaú é bom                    O                                    True   Banco         True         True          False           False        False             False         True       True        False        False              False           False             False        False        True        False        False      pt           do     de o          False        False        False       do           0        False            {'Definite': 'Def', 'Gender': 'Masc', 'Number': 'Sing', 'PronType': 'Art'}      do      do    ADP         d  18446744073709551615            do  (Rede, do, Banco, Itaú, é, bom)            -1           0.0       xx        do    ADP  (Banco, Rede, bom)          ()         ()        ()                            (do,)    (, I, O, B)         Masc         Sing            Def            Art       <NA>          <NA>        <NA>           <NA>
    2       nmod  Rede do Banco Itaú é bom                    B                      LOC           True    Rede         True         True          False           False        False             False        False       True        False        False              False           False             False        False       False         True        False      pt           do    Banco          False        False        False    banco           1         True                                                  {'Gender': 'Masc', 'Number': 'Sing'}   banco   Banco  PROPN         B  18446744073709551615          Itaú  (Rede, do, Banco, Itaú, é, bom)            -1           0.0    Xxxxx       nco  PROPN         (Rede, bom)  (do, Itaú)      (do,)   (Itaú,)                (do, Banco, Itaú)    (, I, O, B)         Masc         Sing           <NA>           <NA>       <NA>          <NA>        <NA>           <NA>
    3  flat:name  Rede do Banco Itaú é bom                    I                      LOC           True   Banco         True        False          False           False        False             False        False       True        False        False              False           False             False        False       False         True        False      pt         Itaú     Itaú          False        False        False     itaú           0        False                                                                    {'Number': 'Sing'}    itaú    Itaú  PROPN         I  18446744073709551615          Itaú  (Rede, do, Banco, Itaú, é, bom)            -1           0.0     Xxxx       taú  PROPN  (Banco, Rede, bom)          ()         ()        ()                          (Itaú,)    (, I, O, B)         <NA>         Sing           <NA>           <NA>       <NA>          <NA>        <NA>           <NA>
    4        cop  Rede do Banco Itaú é bom                    O                                    True     bom         True        False          False           False        False             False         True       True        False        False              False           False             False        False        True        False        False      pt            é      ser          False        False        False        é           0        False  {'Mood': 'Ind', 'Number': 'Sing', 'Person': '3', 'Tense': 'Pres', 'VerbForm': 'Fin'}       é       é    AUX         é  18446744073709551615             é  (Rede, do, Banco, Itaú, é, bom)            -1           0.0        x         é    AUX              (bom,)          ()         ()        ()                             (é,)    (, I, O, B)         <NA>         Sing           <NA>           <NA>        Ind             3        Pres            Fin
    5       ROOT  Rede do Banco Itaú é bom                    O                                    True     bom         True         True          False           False        False             False         True       True        False        False              False            True             False        False        True        False        False      pt         Rede      bom          False        False        False      bom           2        False                                                  {'Gender': 'Masc', 'Number': 'Sing'}     bom     bom    ADJ         b  18446744073709551615           bom  (Rede, do, Banco, Itaú, é, bom)            -1           0.0      xxx       bom    ADJ                  ()   (Rede, é)  (Rede, é)        ()  (Rede, do, Banco, Itaú, é, bom)    (, I, O, B)         Masc         Sing           <NA>           <NA>       <NA>          <NA>        <NA>           <NA>

    """

    worddict = nested_di()
    tocheck_attrs = [
        "dep_",
        "doc",
        "ent_id_",
        "ent_iob_",
        "ent_kb_id_",
        "ent_type_",
        "has_vector",
        "head",
        "is_alpha",
        "is_ascii",
        "is_bracket",
        "is_currency",
        "is_digit",
        "is_left_punct",
        "is_lower",
        "is_oov",
        "is_punct",
        "is_quote",
        "is_right_punct",
        "is_sent_end",
        "is_sent_start",
        "is_space",
        "is_stop",
        "is_title",
        "is_upper",
        "lang_",
        "left_edge",
        "lemma_",
        "like_email",
        "like_num",
        "like_url",
        "lower_",
        "n_lefts",
        "n_rights",
        "morph",
        "norm_",
        "orth_",
        "pos_",
        "prefix_",
        "rank",
        "right_edge",
        "sent",
        "sent_start",
        "sentiment",
        "shape_",
        "suffix_",
        "tag_",
    ]

    for ini, d in enumerate(doc):
        for t in tocheck_attrs:
            try:
                worddict[ini][t.strip("_")] = getattr(d, t)
            except Exception as fe:
                print(fe)
                worddict[ini][t.strip("_")] = None

    tocheck_gens = [
        "ancestors",
        "children",
        "lefts",
        "rights",
        "subtree",
    ]
    for ini, d in enumerate(doc):
        for t in tocheck_gens:
            try:
                worddict[ini][t.strip("_")] = tuple(getattr(d, t))
            except Exception as fe:
                print(fe)
                worddict[ini][t.strip("_")] = None

    tocheck_funcs = ["iob_strings"]

    for ini, d in enumerate(doc):
        for t in tocheck_funcs:
            try:
                worddict[ini][t.strip("_")] = getattr(d, t)()
            except Exception as fe:
                print(fe)
                worddict[ini][t.strip("_")] = None

    df = pd.DataFrame(worddict).T.copy()
    for key, item in dtypes.items():
        try:
            df[key] = df[key].astype(item)
        except Exception as fe:
            print(key)
            print(fe)
            continue

    df["doc"] = df["doc"].ds_apply_ignore(pd.NA, lambda x: str(x))
    df["right_edge"] = df["right_edge"].ds_apply_ignore(pd.NA, lambda x: str(x))
    df["left_edge"] = df["left_edge"].ds_apply_ignore(pd.NA, lambda x: str(x))
    df["head"] = df["head"].ds_apply_ignore(pd.NA, lambda x: str(x))
    df["sent"] = df["sent"].ds_apply_ignore(pd.NA, lambda x: str(x))

    df["doc"] = df["doc"].astype("category")
    df["right_edge"] = df["right_edge"].astype("string")
    df["left_edge"] = df["left_edge"].astype("string")
    df["head"] = df["head"].astype("string")
    df["sent"] = df["sent"].astype("string")

    df.columns = [f"{colprefix}{x}" for x in df.columns]

    df.aa_morph = df.aa_morph.ds_apply_ignore(pd.NA, lambda x: x.to_dict())
    for m in list(dict_merger(*df.aa_morph.dropna().to_list()).keys()):
        df[f"morph_{m}"] = pd.NA
    for ini, li in zip(df.index.to_list(), tuple(df.aa_morph.to_list())):
        if isinstance(li, dict):
            for key, item in li.items():
                df.at[ini, f"morph_{key}"] = item

    morphcols = [x for x in df.columns if x.startswith("morph_")]
    df3 = df[morphcols].copy()
    df4 = df3.ds_reduce_memory_size_carefully(verbose=False)
    df = df.drop(columns=morphcols)
    df = pd.concat([df, df4], axis=1)
    return df
