"""
難病(指定難病, 小児特定慢性疾病)とMondoを紐付ける
"""
import json
from pathlib import Path
from typing import List

from pymondo.mondo import Mondo, MondoNode, Scope
from pynando.nando import Nando, NandoNode
from cnorm.chain import Chain

from .config import Config
from .utils.chain import chain


def _make_mondo_mapper(
        mondo_obj: Mondo, chain: Chain,
        allowed_scope_list: List[Scope],
        allow_deprecated: bool
):
    """return the list of mondos which contain the pattern
    :param mondo_obj:
    :param chain: the chain of rules which is applied to text
    :param allowed_scope_list: the list of scope list
    :param allow_deprecated: use deprecated mondo
    :return:
    """
    mapper = {}
    for mondo_node in mondo_obj:
        _id = mondo_node.id
        if not allow_deprecated and mondo_node.deprecated:
            continue

        text = chain.apply(mondo_node.name)
        mapper.setdefault(text, set())
        mapper[text].add(_id)

        for synonym in mondo_node.synonyms:
            if synonym.scope not in allowed_scope_list:
                continue
            text = chain.apply(synonym.name)
            mapper.setdefault(text, set())
            mapper[text].add(_id)
    mapper.pop('', None)
    return mapper


def _search_mondoids4nando(nando_node: NandoNode, mondo_mapper, chain: Chain):
    """return the mondo ids which match to the nando names"""
    names = [nando_node.name_en] + nando_node.synonyms_en
    mondo_ids = []
    for name in names:
        name = chain.apply(name)
        mondo_ids += mondo_mapper.get(name, [])
    return sorted(list(set(mondo_ids)))


def _mondo_node_to_dict(mondo_node: MondoNode):
    """convert mondo node to dict"""
    mondo_dict = {
        'id': mondo_node.id,
        'name': mondo_node.name,
        'xrefs': mondo_node.xrefs,
        'synonyms': [
            {
                'name': s.name,
                'scope': s.scope.name,
                'xrefs': s.xrefs,
            }
            for s in mondo_node.synonyms
        ]
    }
    return mondo_dict


def _nando_node2dict(nando_node: NandoNode):
    """convert nando node to dict"""
    nando_dict = {
        'id': nando_node.id,
        'name_ja': nando_node.name_ja,
        'synonyms_ja': nando_node.synonyms_ja,
        'name_en': nando_node.name_en,
        'synonyms_en': nando_node.synonyms_en,
        'is_defined_by': nando_node.is_defined_by,
        'see_also': nando_node.see_also,
        'children': sorted([n.id for n in nando_node.children]),
        'class_id': nando_node.class_id,
        'notification_no': nando_node.notification_no,
        'mondo_nodes': nando_node.mondo_nodes,
     }
    return nando_dict


def link_nando2mondo(
        nando_obj: Nando, mondo_obj: Mondo, chain: Chain,
        allowed_scope_list: List[Scope], allow_deprecated: bool
):
    """link the mondo nodes to the nando nodes by comparing the each name"""
    # make a mapper which maps a preprocessed name to the mondo ids
    mondo_mapper = _make_mondo_mapper(
        mondo_obj, chain,
        allowed_scope_list, allow_deprecated
    )

    # link the mondo nodes to each nando node
    for nando_node in nando_obj:
        mondo_ids = _search_mondoids4nando(nando_node, mondo_mapper, chain)
        mondo_nodes = [mondo_obj[_id] for _id in mondo_ids]
        nando_node.mondo_nodes = [_mondo_node_to_dict(m) for m in mondo_nodes]
    return nando_obj


def save(nando_obj: Nando, fp: Path):
    with fp.open(mode='w') as f:
        json.dump([_nando_node2dict(n) for n in nando_obj], f, indent=4, ensure_ascii=False)


def main(target: str):
    assert target in ['nanbyo', 'shoman']

    config = Config()
    results_dir = config.RESULTS_DIR
    data_dir = config.DATA_DIR
    if not results_dir.exists():
        results_dir.mkdir()

    suffix = ''
    allowed_scope_list = []
    if config.ALLOW_EXACT:
        allowed_scope_list.append(Scope.EXACT)
        suffix += 'e'
    if config.ALLOW_BROAD:
        allowed_scope_list.append(Scope.BROAD)
        suffix += 'b'
    if config.ALLOW_NARROW:
        allowed_scope_list.append(Scope.NARROW)
        suffix += 'n'
    if config.ALLOW_RELATED:
        allowed_scope_list.append(Scope.RELATED)
        suffix += 'r'

    nando_obj = link_nando2mondo(
        Nando(target, data_dir),
        Mondo(),
        chain,
        allowed_scope_list,
        config.ALLOW_DEPRECATED
    )

    if suffix:
        file_name = '{}2mondo_{}.json'.format(target, suffix)
    else:
        file_name = '{}2mondo.json'.format(target)
    save(nando_obj, results_dir / file_name)
