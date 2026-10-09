// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Manual: Cooperacre Matriz',
			description: 'Catálogo e governança dos sistemas internos da Cooperacre.',
			defaultLocale: 'root',
			locales: { root: { label: 'Português (BR)', lang: 'pt-BR' } },
			favicon: '/favicon.png',
			logo: {
				src: './src/assets/logo.png',
				alt: 'Cooperacre',
			},
			social: [],
			customCss: ['./src/styles/custom.css'],
			head: [
				{ tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.googleapis.com' } },
				{ tag: 'link', attrs: { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' } },
				{ tag: 'link', attrs: { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Nunito:wght@700;800&display=swap' } },
				{
					tag: 'script',
					content: `
						function cxRealcarPagina() {
							document.querySelectorAll('.tabela-linha-tempo table, .tabela-resumo table').forEach((table) => {
								const headers = Array.from(table.querySelectorAll('thead th')).map((th) => th.textContent.trim());
								table.querySelectorAll('tbody tr').forEach((tr) => {
									Array.from(tr.children).forEach((td, i) => {
										if (headers[i]) td.setAttribute('data-th', headers[i]);
									});
								});
							});
							let overlay = document.querySelector('.cx-lightbox');
							if (!overlay) {
								overlay = document.createElement('div');
								overlay.className = 'cx-lightbox';
								overlay.innerHTML = '<img alt="">';
								overlay.addEventListener('click', () => overlay.classList.remove('cx-lightbox--aberto'));
								document.addEventListener('keydown', (e) => {
									if (e.key === 'Escape') overlay.classList.remove('cx-lightbox--aberto');
								});
								document.body.appendChild(overlay);
							}
							const overlayImg = overlay.querySelector('img');
							document.querySelectorAll('.sl-markdown-content img').forEach((img) => {
								if (img.closest('a') || img.dataset.cxLightboxLigado) return;
								img.dataset.cxLightboxLigado = '1';
								img.style.cursor = 'zoom-in';
								img.addEventListener('click', () => {
									overlayImg.src = img.currentSrc || img.src;
									overlayImg.alt = img.alt || '';
									overlay.classList.add('cx-lightbox--aberto');
								});
							});
							// Agrupa legenda + print numa figura, para a impressão não separar os dois
							document.querySelectorAll('.sl-markdown-content > p > img:only-child').forEach((img) => {
								const pImg = img.parentElement;
								const legenda = pImg.previousElementSibling;
								if (pImg.parentElement.classList.contains('cx-figura')) return;
								const grupo = document.createElement('div');
								grupo.className = 'cx-figura';
								pImg.before(grupo);
								if (legenda && legenda.tagName === 'P' && !legenda.querySelector('img')) grupo.appendChild(legenda);
								grupo.appendChild(pImg);
								img.loading = 'eager';
							});
							// Botão de impressão nas fichas (páginas com selo de estágio)
							const conteudo = document.querySelector('.sl-markdown-content');
							if (conteudo && conteudo.querySelector('.selos') && !document.querySelector('.cx-imprimir')) {
								const botao = document.createElement('button');
								botao.type = 'button';
								botao.className = 'cx-imprimir';
								botao.textContent = '🖨 Imprimir ficha / salvar em PDF';
								botao.addEventListener('click', () => window.print());
								conteudo.insertBefore(botao, conteudo.firstChild);
							}
							// Só no papel: o protocolo fica isolado da ficha, na última página.
							// A ficha é informativa e pode evoluir; este registro formaliza o sistema.
							if (conteudo && conteudo.querySelector('.selos') && !document.querySelector('.cx-protocolo')) {
								const nome = document.querySelector('h1')?.textContent.trim() || 'Sistema';
								const escapar = (texto) => String(texto).replace(/[&<>"']/g, (caractere) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[caractere]);
								const textoDoCard = (titulo) => Array.from(conteudo.querySelectorAll('.card')).find((card) => card.querySelector('.title')?.textContent.trim() === titulo)?.querySelector('.body')?.textContent.trim() || 'A confirmar antes da assinatura.';
								const tituloFinalidade = Array.from(conteudo.querySelectorAll('h2')).find((titulo) => titulo.textContent.trim() === 'Em uma frase');
								const finalidade = tituloFinalidade?.closest('.sl-heading-wrapper')?.nextElementSibling?.textContent.trim() || 'A confirmar antes da assinatura.';
								const solicitante = textoDoCard('Quem pediu');
								const situacao = Array.from(conteudo.querySelectorAll('.selos .sl-badge')).map((selo) => selo.textContent.trim()).join(' · ') || 'A confirmar antes da assinatura.';
								const identificador = nome.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-|-$/g, '').toUpperCase();
								const protocolo = document.createElement('section');
								protocolo.className = 'cx-protocolo';
								protocolo.innerHTML = '<p class="cx-protocolo-marca">Cooperacre · Manual de Sistemas</p>' +
									'<h2>Protocolo de registro do sistema</h2>' +
									'<p class="cx-protocolo-intro">Registro formal do item documentado nesta ficha.</p>' +
									'<table class="cx-protocolo-tabela"><tbody>' +
									'<tr><th>Código do protocolo</th><td><strong>PROJ-' + identificador + '-2026</strong></td></tr>' +
									'<tr><th>Nome do sistema</th><td><strong>' + escapar(nome) + '</strong></td></tr>' +
									'<tr><th>Solicitante / área</th><td>' + escapar(solicitante) + '</td></tr>' +
									'<tr><th>Finalidade no registro</th><td class="cx-protocolo-campo-longo">' + escapar(finalidade) + '</td></tr>' +
									'<tr><th>Responsável técnico</th><td><strong>Lucas Castro</strong>, T.I.</td></tr>' +
									'<tr><th>Situação no registro</th><td>' + escapar(situacao) + '</td></tr>' +
									'</tbody></table>' +
									'<p class="cx-protocolo-declaracao">Este protocolo formaliza a existência e a responsabilidade pelo sistema identificado acima. A ficha que o antecede é informativa e retrata a versão consultada nesta emissão; ela poderá ser atualizada sem alterar este registro.</p>' +
									'<div class="cx-protocolo-local"><span>Local</span><i></i><span>Data</span><i></i></div>' +
									'<div class="cx-protocolo-assinaturas">' +
									'<div><i></i><strong>Edinar</strong><span>Gerente administrativa</span></div>' +
									'<div><i></i><strong>Lucas Castro</strong><span>T.I., responsável técnico</span></div>' +
									'</div>' +
									'<p class="cx-protocolo-rodape">Emitido em duas vias de igual teor: uma para a gestão e uma para o responsável técnico.</p>';
								conteudo.appendChild(protocolo);
							}
							// Card com pouco texto (ex.: só um nome ou cargo) fica com o corpo
							// centralizado, em vez de justificado com poucas palavras esparramadas.
							document.querySelectorAll('.sl-markdown-content .card .body').forEach((body) => {
								body.classList.toggle('cx-card-curto', body.textContent.trim().length < 60);
							});
						}
						document.addEventListener('astro:page-load', cxRealcarPagina);
						if (document.readyState === 'loading') {
							document.addEventListener('DOMContentLoaded', cxRealcarPagina);
						} else {
							cxRealcarPagina();
						}
					`,
				},
			],
			sidebar: [
				{
					label: 'Introdução',
					items: [
						{ label: 'O que é este manual', slug: 'intro' },
						{ label: 'Glossário', slug: 'glossario' },
					],
				},
				{
					label: 'Catálogo de Sistemas',
					items: [
						{ label: 'Visão geral', slug: 'catalogo' },
						{ label: 'Por situação', slug: 'catalogo/situacao' },
						{ label: 'Onde está o código', slug: 'catalogo/repositorios' },
						{ label: 'Modelo de ficha', slug: 'catalogo/modelo-de-ficha' },
					],
				},
				{
					label: 'Sistemas',
					items: [
						{ label: 'Visão geral', slug: 'sistemas' },
						{ label: 'Análise Comercial', slug: 'catalogo/analisecomercial' },
						{ label: 'Comissão', slug: 'catalogo/comissao' },
						{ label: 'Consulta Meta', slug: 'catalogo/consultameta' },
						{ label: 'CooperConecta', slug: 'catalogo/cooperconecta' },
						{ label: 'CooperFlow', slug: 'catalogo/cooperflow' },
						{ label: 'Cooperlog', slug: 'catalogo/cooperlog' },
						{ label: 'Net Monitor', slug: 'catalogo/netmonitor' },
					],
				},
				{
					label: 'Planilhas',
					items: [
						{ label: 'Visão geral', slug: 'planilhas' },
						{ label: 'Controle de Saída', slug: 'catalogo/controle-de-saida' },
						{ label: 'Controle Interno', slug: 'planilhas/controle-interno' },
						{ label: 'Estoque Polpa', slug: 'catalogo/estoquepolpa' },
						{ label: 'Transferência Estoque Balcão', slug: 'planilhas/transferencia-estoque-balcao' },
					],
				},
				{
					label: 'Automações',
					items: [
						{ label: 'Visão geral', slug: 'automacoes' },
						{ label: 'Meta Pipeline', slug: 'catalogo/meta-pipeline' },
						{ label: 'Conciliador Contábil', slug: 'catalogo/contabil' },
						{ label: 'Controle de Vendas', slug: 'catalogo/controledevendas' },
						{ label: 'Conversor de Extrato SICOOB', slug: 'automacoes/pdftoexcel' },
						{ label: 'Formatar Exportação', slug: 'automacoes/formatar-exportacao' },
						{ label: 'Gerador de Cards', slug: 'automacoes/gerador-cards' },
					],
				},
				{
					label: 'Filial IV',
					items: [
						{ label: 'Visão geral', slug: 'catalogo/filial-4' },
						{ label: 'Webapp: versão Veja', slug: 'catalogo/webapp-filial-iv-veja' },
						{ label: 'Webapp: interno', slug: 'catalogo/webapp-filial-iv-interno' },
						{ label: 'Planilha de Contrato', slug: 'catalogo/planilha-contrato-filial-iv' },
						{ label: 'DARB', slug: 'catalogo/darb-filial-iv' },
						{ label: 'Relação de Despesas', slug: 'catalogo/relacao-despesas-filial-iv' },
						{ label: 'Manual Operacional', slug: 'catalogo/manual-filial-iv' },
					],
				},
				{
					label: 'Governança',
					items: [
						{ label: 'Princípios', slug: 'governanca/principios' },
						{ label: 'Acessos e responsabilidades', slug: 'governanca/acessos' },
						{ label: 'Mudanças e versionamento', slug: 'governanca/mudancas' },
						{ label: 'Desenvolvimento com IA', slug: 'governanca/desenvolvimento-com-ia' },
						{ label: 'Vibe coding', slug: 'governanca/vibe-coding' },
						{ label: 'Credenciais e backup', slug: 'governanca/credenciais-e-backup' },
					],
				},
			],
		}),
		mdx(),
	],
});
