import { useCallback, useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE_URL = "http://localhost:5000";
const ABAS = ["Operações", "Filmes", "Clientes", "Aluguéis"];

async function requisicaoJson(endpoint, options = {}) {
  const resposta = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  const texto = await resposta.text();
  const dados = texto ? JSON.parse(texto) : null;

  if (!resposta.ok) {
    const mensagemErro =
      typeof dados === "string"
        ? dados
        : dados?.erro || dados?.mensagem || "Não foi possível concluir a operação.";
    throw new Error(mensagemErro);
  }

  return dados;
}

function formatarData(valor) {
  if (!valor) {
    return "--";
  }

  const data = new Date(valor);

  if (Number.isNaN(data.getTime())) {
    return String(valor);
  }

  return data.toLocaleDateString("pt-BR");
}

function App() {
  const [filmes, setFilmes] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [alugueis, setAlugueis] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");
  const [abaAtiva, setAbaAtiva] = useState("Operações");

  const [filmeForm, setFilmeForm] = useState({
    titulo: "",
    genero: "",
    ano: "",
  });
  const [clienteForm, setClienteForm] = useState({
    nome: "",
    telefone: "",
    email: "",
  });
  const [aluguelForm, setAluguelForm] = useState({
    cliente_id: "",
    filme_id: "",
  });
  const [devolucaoForm, setDevolucaoForm] = useState({
    aluguel_id: "",
  });

  function limparFeedback() {
    setMensagem("");
    setErro("");
  }

  const carregarFilmes = useCallback(async () => {
    const dados = await requisicaoJson("/filmes", { method: "GET" });
    setFilmes(dados);
  }, []);

  const carregarClientes = useCallback(async () => {
    const dados = await requisicaoJson("/clientes", { method: "GET" });
    setClientes(dados);
  }, []);

  const carregarAlugueis = useCallback(async () => {
    const dados = await requisicaoJson("/alugueis", { method: "GET" });
    setAlugueis(dados);
  }, []);

  const carregarDados = useCallback(async () => {
    setCarregando(true);
    limparFeedback();

    try {
      await Promise.all([carregarFilmes(), carregarClientes(), carregarAlugueis()]);
    } catch (error) {
      setErro(error.message);
    } finally {
      setCarregando(false);
    }
  }, [carregarAlugueis, carregarClientes, carregarFilmes]);

  useEffect(() => {
    const timer = setTimeout(() => {
      void carregarDados();
    }, 0);

    return () => clearTimeout(timer);
  }, [carregarDados]);

  const estatisticas = useMemo(() => {
    const filmesDisponiveis = filmes.filter((filme) => filme.disponivel).length;
    const filmesAlugados = filmes.length - filmesDisponiveis;

    return {
      filmes: [
        { label: "Cadastrados", valor: filmes.length, classe: "neutral" },
        { label: "Disponíveis", valor: filmesDisponiveis, classe: "free" },
        { label: "Alugados", valor: filmesAlugados, classe: "busy" },
      ],
      resumo: [{ label: "Clientes", valor: clientes.length, destaque: "cadastros totais" }],
    };
  }, [clientes.length, filmes]);

  function atualizarCampo(setter, campo, valor) {
    setter((estadoAtual) => ({
      ...estadoAtual,
      [campo]: valor,
    }));
  }

  async function cadastrarFilme(event) {
    event.preventDefault();
    limparFeedback();

    try {
      const dados = await requisicaoJson("/filmes", {
        method: "POST",
        body: JSON.stringify({
          titulo: filmeForm.titulo,
          genero: filmeForm.genero,
          ano: Number(filmeForm.ano),
        }),
      });

      setMensagem(dados?.mensagem || "Filme cadastrado com sucesso.");
      setFilmeForm({ titulo: "", genero: "", ano: "" });
      await carregarFilmes();
      setAbaAtiva("Filmes");
    } catch (error) {
      setErro(error.message);
    }
  }

  async function cadastrarCliente(event) {
    event.preventDefault();
    limparFeedback();

    try {
      const dados = await requisicaoJson("/clientes", {
        method: "POST",
        body: JSON.stringify(clienteForm),
      });

      setMensagem(
        typeof dados === "string" ? dados : "Cliente cadastrado com sucesso."
      );
      setClienteForm({ nome: "", telefone: "", email: "" });
      await carregarClientes();
      setAbaAtiva("Clientes");
    } catch (error) {
      setErro(error.message);
    }
  }

  async function alugarFilme(event) {
    event.preventDefault();
    limparFeedback();

    try {
      const dados = await requisicaoJson("/alugueis", {
        method: "POST",
        body: JSON.stringify({
          cliente_id: Number(aluguelForm.cliente_id),
          filme_id: Number(aluguelForm.filme_id),
        }),
      });

      setMensagem(dados?.mensagem || "Filme alugado com sucesso.");
      setAluguelForm({ cliente_id: "", filme_id: "" });
      await carregarDados();
      setAbaAtiva("Aluguéis");
    } catch (error) {
      setErro(error.message);
    }
  }

  async function devolverFilme(event) {
    event.preventDefault();
    limparFeedback();

    try {
      const dados = await requisicaoJson("/devolucoes", {
        method: "POST",
        body: JSON.stringify({
          aluguel_id: Number(devolucaoForm.aluguel_id),
        }),
      });

      setMensagem(dados?.mensagem || "Filme devolvido com sucesso.");
      setDevolucaoForm({ aluguel_id: "" });
      await carregarDados();
      setAbaAtiva("Aluguéis");
    } catch (error) {
      setErro(error.message);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">Sistema de locadora</p>
          <h1>Cadastro, aluguel e devolução de filmes em uma interface simples</h1>
          <p className="hero-text">
            Montei esse projeto para praticar a integração entre frontend,
            backend e banco de dados em um fluxo básico de locadora.
          </p>
        </div>

        <div className="hero-actions">
          <button className="secondary-button" type="button" onClick={carregarDados}>
            Atualizar dados
          </button>
        </div>
      </section>

      <section className="stats-grid">
        <article className="stats-panel film-panel">
          <div className="stats-panel-header">
            <span>Filmes</span>
            <small>Visão rápida do acervo</small>
          </div>

          <div className="mini-stats-grid">
            {estatisticas.filmes.map((item) => (
              <div className={`mini-stat-card ${item.classe}`} key={item.label}>
                <span>{item.label}</span>
                <strong>{item.valor}</strong>
              </div>
            ))}
          </div>
        </article>

        <div className="summary-stats">
          {estatisticas.resumo.map((item) => (
            <article className="stat-card" key={item.label}>
              <span>{item.label}</span>
              <strong>{item.valor}</strong>
              <small>{item.destaque}</small>
            </article>
          ))}
        </div>
      </section>

      {mensagem ? <div className="feedback success">{mensagem}</div> : null}
      {erro ? <div className="feedback error">{erro}</div> : null}

      <section className="tabs-bar">
        {ABAS.map((aba) => (
          <button
            key={aba}
            type="button"
            className={abaAtiva === aba ? "tab-button active" : "tab-button"}
            onClick={() => setAbaAtiva(aba)}
          >
            {aba}
          </button>
        ))}
      </section>

      {abaAtiva === "Operações" ? (
        <section className="dashboard-grid">
          <article className="card">
            <div className="card-header">
              <h2>Cadastrar filme</h2>
              <span>Inclui título, gênero e ano</span>
            </div>
            <form className="stack-form" onSubmit={cadastrarFilme}>
              <label>
                <span>Título</span>
                <input
                  type="text"
                  placeholder="Ex: Cidade de Deus"
                  value={filmeForm.titulo}
                  onChange={(event) =>
                    atualizarCampo(setFilmeForm, "titulo", event.target.value)
                  }
                />
              </label>
              <label>
                <span>Gênero</span>
                <input
                  type="text"
                  placeholder="Ex: Drama"
                  value={filmeForm.genero}
                  onChange={(event) =>
                    atualizarCampo(setFilmeForm, "genero", event.target.value)
                  }
                />
              </label>
              <label>
                <span>Ano</span>
                <input
                  type="number"
                  placeholder="Ex: 2002"
                  value={filmeForm.ano}
                  onChange={(event) =>
                    atualizarCampo(setFilmeForm, "ano", event.target.value)
                  }
                />
              </label>
              <button className="primary-button" type="submit">
                Salvar filme
              </button>
            </form>
          </article>

          <article className="card">
            <div className="card-header">
              <h2>Cadastrar cliente</h2>
              <span>Nome, telefone e email</span>
            </div>
            <form className="stack-form" onSubmit={cadastrarCliente}>
              <label>
                <span>Nome</span>
                <input
                  type="text"
                  placeholder="Ex: Maria Silva"
                  value={clienteForm.nome}
                  onChange={(event) =>
                    atualizarCampo(setClienteForm, "nome", event.target.value)
                  }
                />
              </label>
              <label>
                <span>Telefone</span>
                <input
                  type="text"
                  placeholder="Ex: (11) 99999-9999"
                  value={clienteForm.telefone}
                  onChange={(event) =>
                    atualizarCampo(setClienteForm, "telefone", event.target.value)
                  }
                />
              </label>
              <label>
                <span>Email</span>
                <input
                  type="email"
                  placeholder="cliente@email.com"
                  value={clienteForm.email}
                  onChange={(event) =>
                    atualizarCampo(setClienteForm, "email", event.target.value)
                  }
                />
              </label>
              <button className="primary-button" type="submit">
                Salvar cliente
              </button>
            </form>
          </article>

          <article className="card">
            <div className="card-header">
              <h2>Alugar filme</h2>
              <span>Seleciona cliente e filme disponível</span>
            </div>
            <form className="stack-form" onSubmit={alugarFilme}>
              <label>
                <span>Cliente</span>
                <select
                  value={aluguelForm.cliente_id}
                  onChange={(event) =>
                    atualizarCampo(setAluguelForm, "cliente_id", event.target.value)
                  }
                >
                  <option value="">Selecione o cliente</option>
                  {clientes.map((cliente) => (
                    <option key={cliente.id} value={cliente.id}>
                      {cliente.nome} #{cliente.id}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                <span>Filme</span>
                <select
                  value={aluguelForm.filme_id}
                  onChange={(event) =>
                    atualizarCampo(setAluguelForm, "filme_id", event.target.value)
                  }
                >
                  <option value="">Selecione o filme</option>
                  {filmes
                    .filter((filme) => filme.disponivel)
                    .map((filme) => (
                      <option key={filme.id} value={filme.id}>
                        {filme.titulo} #{filme.id}
                      </option>
                    ))}
                </select>
              </label>
              <button className="primary-button" type="submit">
                Registrar aluguel
              </button>
            </form>
          </article>

          <article className="card">
            <div className="card-header">
              <h2>Devolver filme</h2>
              <span>Fecha um aluguel em andamento</span>
            </div>
            <form className="stack-form" onSubmit={devolverFilme}>
              <label>
                <span>Aluguel</span>
                <select
                  value={devolucaoForm.aluguel_id}
                  onChange={(event) =>
                    atualizarCampo(setDevolucaoForm, "aluguel_id", event.target.value)
                  }
                >
                  <option value="">Selecione o aluguel</option>
                  {alugueis
                    .filter((aluguel) => !aluguel.devolvido)
                    .map((aluguel) => (
                      <option key={aluguel.id} value={aluguel.id}>
                        {aluguel.filme} - {aluguel.cliente} #{aluguel.id}
                      </option>
                    ))}
                </select>
              </label>
              <button className="primary-button" type="submit">
                Confirmar devolução
              </button>
            </form>
          </article>
        </section>
      ) : null}

      {abaAtiva === "Filmes" ? (
        <section className="panel-section">
          <div className="section-heading">
            <div>
              <h2>Acervo de filmes</h2>
              <p>Lista dos filmes cadastrados e status atual de cada um.</p>
            </div>
            <span>{filmes.length} registros</span>
          </div>

          <div className="table-card">
            {carregando ? (
              <p>Carregando filmes...</p>
            ) : (
              <div className="table-shell">
                <div className="table-row table-head">
                  <span>ID</span>
                  <span>Título</span>
                  <span>Gênero</span>
                  <span>Ano</span>
                  <span>Status</span>
                </div>
                {filmes.map((filme) => (
                  <div className="table-row" key={filme.id}>
                    <span>#{filme.id}</span>
                    <strong>{filme.titulo}</strong>
                    <span>{filme.genero}</span>
                    <span>{filme.ano}</span>
                    <span
                      className={filme.disponivel ? "status-badge free" : "status-badge busy"}
                    >
                      {filme.disponivel ? "Disponível" : "Alugado"}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      ) : null}

      {abaAtiva === "Clientes" ? (
        <section className="panel-section">
          <div className="section-heading">
            <div>
              <h2>Base de clientes</h2>
              <p>Clientes cadastrados para usar no fluxo de locação.</p>
            </div>
            <span>{clientes.length} registros</span>
          </div>

          <div className="list-grid">
            {clientes.map((cliente) => (
              <article className="list-card" key={cliente.id}>
                <small>Cliente #{cliente.id}</small>
                <strong>{cliente.nome}</strong>
                <span>{cliente.telefone}</span>
                <span>{cliente.email}</span>
              </article>
            ))}
          </div>
        </section>
      ) : null}

      {abaAtiva === "Aluguéis" ? (
        <section className="panel-section">
          <div className="section-heading">
            <div>
              <h2>Painel de aluguéis</h2>
              <p>Resumo dos aluguéis registrados e da previsão de devolução.</p>
            </div>
            <span>{alugueis.length} registros</span>
          </div>

          <div className="list-grid rentals-grid">
            {alugueis.map((aluguel) => (
              <article className="list-card rental-card" key={aluguel.id}>
                <div className="rental-topline">
                  <small>Aluguel #{aluguel.id}</small>
                  <span
                    className={
                      aluguel.devolvido ? "status-badge returned" : "status-badge busy"
                    }
                  >
                    {aluguel.devolvido ? "Devolvido" : "Em andamento"}
                  </span>
                </div>
                <strong>{aluguel.filme}</strong>
                <span>Cliente: {aluguel.cliente}</span>
                <span>Alugado em: {formatarData(aluguel.data_aluguel)}</span>
                <span>Previsão: {formatarData(aluguel.data_devolucao)}</span>
              </article>
            ))}
          </div>
        </section>
      ) : null}
    </main>
  );
}

export default App;
