"""Sobe imagens para o Files da Shopify e imprime as URLs do CDN.

    python tools/upload_shopify.py pep-protein.myshopify.com check pep-bv-
    python tools/upload_shopify.py pep-protein.myshopify.com upload pep/assets/boas-vindas a.jpg b.png

Antes, uma vez por loja (abre o navegador para autorizar):
    shopify store auth --store pep-protein.myshopify.com --scopes read_files,write_files

Fluxo: stagedUploadsCreate -> POST multipart do arquivo -> fileCreate -> espera ficar READY.
SEMPRE rode `check` com o prefixo antes: se o nome já existe, a Shopify renomeia o novo
(nome_<uuid>.png) e a URL do template quebra.
"""
import json, mimetypes, os, subprocess, sys, time
import requests

store, mode = sys.argv[1], sys.argv[2]
env = dict(os.environ, SHOPIFY_CLI_AGENT_INFO='n:claude-code|v:unknown|p:anthropic')


def gql(query, variables=None, mutation=False):
    cmd = ['shopify', 'store', 'execute', '--store', store, '--query', query, '--json']
    if variables is not None:
        cmd += ['--variables', json.dumps(variables)]
    if mutation:
        cmd.append('--allow-mutations')
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', env=env, shell=True)
    if r.returncode != 0:
        sys.exit(f'CLI error: {r.stdout}\n{r.stderr}')
    res = json.loads(r.stdout[r.stdout.index('{'):])
    return res.get('data', res)


if mode == 'check':
    q = 'query($q:String!){ files(first:50, query:$q){ nodes { ... on MediaImage { image { url } } ... on GenericFile { url } } } }'
    for n in gql(q, {'q': f'filename:{sys.argv[3]}*'})['files']['nodes']:
        print((n.get('image') or {}).get('url') or n.get('url'))
    sys.exit()

folder, names = sys.argv[3], sys.argv[4:]
inputs = [{'filename': f, 'mimeType': mimetypes.guess_type(f)[0], 'resource': 'IMAGE', 'httpMethod': 'POST',
           'fileSize': str(os.path.getsize(os.path.join(folder, f)))} for f in names]
st = gql('mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){ stagedTargets { url resourceUrl parameters { name value } } userErrors { message } } }',
         {'input': inputs}, mutation=True)['stagedUploadsCreate']
if st['userErrors']:
    sys.exit(st['userErrors'])
for f, t in zip(names, st['stagedTargets']):
    with open(os.path.join(folder, f), 'rb') as fh:
        requests.post(t['url'], data={p['name']: p['value'] for p in t['parameters']},
                      files={'file': (f, fh, mimetypes.guess_type(f)[0])}).raise_for_status()
fc = gql('mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){ files { id } userErrors { message } } }',
         {'files': [{'originalSource': t['resourceUrl'], 'filename': f, 'contentType': 'IMAGE', 'alt': f}
                    for f, t in zip(names, st['stagedTargets'])]}, mutation=True)['fileCreate']
if fc['userErrors']:
    sys.exit(fc['userErrors'])
ids = [x['id'] for x in fc['files']]
for _ in range(30):
    time.sleep(3)
    nodes = gql('query($ids:[ID!]!){ nodes(ids:$ids){ ... on MediaImage { fileStatus image { url } } } }', {'ids': ids})['nodes']
    if all(n['fileStatus'] == 'READY' and n.get('image') for n in nodes):
        break
for f, n in zip(names, nodes):
    print(f, n['fileStatus'], (n.get('image') or {}).get('url'))
