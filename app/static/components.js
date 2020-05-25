import { html, render, Component } from 'https://unpkg.com/htm/preact/standalone.module.js';

const API = {
  token: null,
  base: null,
  init: (apiUrl, token) => {
    API.base = apiUrl;
    API.token = token;
  },
  call: async (url, method = 'GET', data) => {
    const headers = { ...(API.token && { Authorization: `Bearer ${API.token}` }) };
    const body = data ? JSON.stringify(data) : undefined;
    const r = await fetch(API.base + url, { method, headers, body }).catch(err => ({ json: () => err }));
    if (!r.ok) throw r.json();
    return r.json();
  },
  post: async (url, data) => API.call(url, 'POST', data),
  patch: async (url, data) => API.call(url, 'PATCH', data),
  delete: async url => API.call(url, 'DELETE').catch(() => null),
  getPermissions: () => API.call('/user').then(({ permissions }) => permissions),
  getMovies: () => API.call('/movies').then(({ movies }) => movies),
  createMovie: data => API.post('/movies', data).then(({ movie }) => movie),
  updateMovie: movie => API.patch(`/movies/${movie.id}`, movie).then(({ movie }) => movie),
  deleteMovie: movie => API.delete(`/movies/${movie.id}`),
  getActors: () => API.call('/actors').then(({ actors }) => actors),
  createActor: data => API.post('/actors', data).then(({ actor }) => actor),
  updateActor: actor => API.patch(`/actors/${actor.id}`, actor).then(({ actor }) => actor),
  deleteActor: actor => API.delete(`/actors/${actor.id}`),
};

const getHashToken = url => {
  const url1 = new URL(url);
  if (!url1.hash) return;
  const url2 = new URL(url1.hash.replace('#', url1.origin + '/?'));
  return url2.searchParams.get('access_token');
};

const Btn = props => {
  return html`<button className="btn ${props.className || ''}" onClick="${props.onClick}">${props.text}</button>`;
};

const Logout = ({ store }) => html`
  <div className="userPerms"><b>You can:</b> ${store.permissions.join(', ')}</div>
  <${Btn} onClick="${store.logout}" text="Logout" />
`;

const Login = ({ store }) => {
  const onClick = () => (window.location.href = store.loginUrl);
  if (!store.token) return html`<${Btn} text="Login" onClick="${onClick}" />`;
  return html`<${Logout} store="${store}" />`;
};

const AppHeader = ({ store }) => {
  return html`<header className="appHeader">
    <h1>
      Udacity Fullstack Capstone Project
      <small>Created by Alex Parra</small>
    </h1>
    <${Login} store="${store}" />
  </header>`;
};

const MoviesList = ({ store }) => {
  const { movies = [] } = store;
  return html`
    <div className="movies listWrap">
      <h2>
        <span>Movies </span>
        ${store.can('movies:create') && html`<${Btn} className="icon" text="+" onClick="${() => store.modalOn('addMovie')}" />`}
      </h2>
      <ol>
        ${movies.map(
          movie => html`<li onClick="${() => store.modalOn('viewMovie', movie)}">
            <h3>${movie.title}</h3>
            <small title="Movie Release Date">${movie.release_date}</small>
            ${store.can('movies:delete') &&
            html`<${Btn} text="×" className="icon danger" onClick="${ev => (ev.stopPropagation(), store.deleteMovie(movie))}" />`}
          </li>`
        )}
      </ol>
    </div>
  `;
};

const MovieDetail = ({ movie, store }) => {
  return html`
    <div className="detailView">
      <h2>
        <span>${movie.title}</span>
        ${store.can('movies:update') && html`<${Btn} className="small" text="Edit" onClick="${() => store.modalOn('editMovie', movie)}" />`}
      </h2>
      <p>Released: ${movie.release_date}</p>
    </div>
  `;
};

class MovieForm extends Component {
  constructor(props) {
    super(props);
    const { movie = { title: '', release_date: '' } } = props;
    this.state = { ...movie };
  }

  render(props, state) {
    const createOrEdit = props.movie ? 'Edit' : 'Create';
    return html`
      <h2>${createOrEdit} Movie</h2>
      <label className="formControl">
        <strong>Title:</strong>
        <input type="text" value="${state.title}" onInput="${ev => this.setState({ title: ev.target.value })}" placeholder="Type movie name" />
      </label>
      <label className="formControl">
        <strong>Release Date:</strong>
        <input
          type="date"
          value="${state.release_date}"
          onInput="${ev => this.setState({ release_date: ev.target.value })}"
          placeholder="Type movie name"
        />
      </label>
      <div className="formActions">
        <${Btn} text="Save" onClick="${() => props.submit(state)}" />
      </div>
    `;
  }
}

const ActorsList = ({ store }) => {
  const { actors = [] } = store;
  return html`
    <div className="actors listWrap">
      <h2>
        <span>Actors</span>
        ${store.can('actors:create') && html`<${Btn} className="icon" text="+" onClick="${() => store.modalOn('addActor')}" />`}
      </h2>
      <ol>
        ${actors.map(
          actor => html`<li onClick="${() => store.modalOn('viewActor', actor)}">
            <h3>${actor.name}</h3>
            <small title="Actor Age">${actor.age}</small>
            ${store.can('actors:delete') &&
            html`<${Btn} text="×" className="icon danger" onClick="${ev => (ev.stopPropagation(), store.deleteActor(actor))}" />`}
          </li>`
        )}
      </ol>
    </div>
  `;
};

const ActorDetail = ({ actor, store }) => {
  return html`
    <div className="detailView">
      <h2>
        <span>${actor.name}</span>
        ${store.can('actors:update') && html`<${Btn} className="small" text="Edit" onClick="${() => store.modalOn('editActor', actor)}" />`}
      </h2>
      <p>Age: ${actor.age}</p>
      <p>Gender: ${actor.gender}</p>
    </div>
  `;
};

class ActorForm extends Component {
  constructor(props) {
    super(props);
    const { actor = { name: '', age: '', gender: '' } } = props;
    this.state = { ...actor };
  }

  render(props, state) {
    const createOrEdit = props.actor ? 'Edit' : 'Create';
    return html`
      <h2>${createOrEdit} Actor</h2>
      <label className="formControl">
        <strong>Name:</strong>
        <input type="text" value="${state.name}" onInput="${ev => this.setState({ name: ev.target.value })}" placeholder="Type actor name" />
      </label>
      <label className="formControl">
        <strong>Age:</strong>
        <input
          type="number"
          min="0"
          max="120"
          placeholder="Enter actor age"
          value="${state.age}"
          onInput="${ev => this.setState({ age: Number(ev.target.value) })}"
        />
      </label>
      <label className="formControl">
        <strong>Gender:</strong>
        <select value="${state.gender}" onChange="${ev => this.setState({ gender: ev.target.value })}">
          <option value="" disabled selected>- Select actor gender -</option>
          <option value="M">Male</option>
          <option value="F">Female</option>
          <option value="X">Non-binary</option>
        </select>
      </label>
      <div className="formActions">
        <${Btn} text="Save" onClick="${() => props.submit(state)}" />
      </div>
    `;
  }
}

class Modal extends Component {
  render() {
    const { store } = this.props;
    const { action, data } = store.modal;
    const modals = {
      addMovie: () => html`<${MovieForm} submit="${store.addMovie}" />`,
      viewMovie: () => html`<${MovieDetail} movie="${data}" store="${store}" />`,
      editMovie: () => html`<${MovieForm} movie="${data}" submit="${store.saveMovie}" />`,
      addActor: () => html`<${ActorForm} submit="${store.addActor}" />`,
      viewActor: () => html`<${ActorDetail} actor="${data}" store="${store}" />`,
      editActor: () => html`<${ActorForm} actor="${data}" submit="${store.saveActor}" />`,
    };

    return html`
      <div className="modal" onClick="${store.modalOff}">
        <div className="content" onClick="${ev => ev.stopPropagation()}">
          ${modals[action]()}
        </div>
      </div>
    `;
  }
}

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { ...this.props, movies: [], actors: [], modal: null };
  }

  componentDidMount() {
    const { appUrl } = this.state;
    const token = getHashToken(window.location.href);
    if (token) {
      sessionStorage.setItem('auth', token);
      this.setState({ token }, this.getData);
      window.history.replaceState(null, null, appUrl);
    } else {
      this.getData();
    }
  }

  logout = () => {
    sessionStorage.removeItem('auth');
    window.location.href = this.state.logoutUrl;
  };

  getMovies = () => API.getMovies().then(movies => this.setState({ movies }));
  getActors = () => API.getActors().then(actors => this.setState({ actors }));
  modalOn = (action, data) => this.setState({ modal: { action, data } });
  modalOff = () => this.setState({ modal: null });

  getData = () => {
    const { apiUrl, token } = this.state;
    if (!token) return;
    API.init(apiUrl, token);
    Promise.all([API.getPermissions(), API.getMovies(), API.getActors()])
      .then(([permissions, movies, actors]) => this.setState({ permissions, movies, actors }))
      .catch(this.logout);
  };

  getStore = state => {
    const { permissions = [] } = state;
    return {
      ...state,
      logout: this.logout,
      modalOff: this.modalOff,
      modalOn: this.modalOn,
      can: perm => permissions.includes(perm),
      addMovie: data => (this.modalOff(), API.createMovie(data).then(this.getMovies)),
      saveMovie: data =>
        API.updateMovie(data).then(movie => {
          this.getMovies().then(this.modalOn('viewMovie', movie));
        }),
      deleteMovie: movie => {
        if (confirm(`Are you sure you want to delete\n${movie.title}`)) {
          API.deleteMovie(movie).then(this.getMovies);
        }
      },
      addActor: data => (this.modalOff(), API.createActor(data).then(this.getActors)),
      saveActor: data =>
        API.updateActor(data).then(actor => {
          this.getActors().then(this.modalOn('viewActor', actor));
        }),
      deleteActor: actor => {
        if (confirm(`Are you sure you want to delete\n${actor.name}`)) {
          API.deleteActor(actor).then(this.getActors);
        }
      },
    };
  };

  render() {
    const store = this.getStore(this.state);
    return html`
      <${AppHeader} store="${store}" />
      ${!store.token
        ? html`<main className="mainLoggedOut">Please login</main>`
        : html`
            <main className="mainLists">
              <${MoviesList} store="${store}" />
              <${ActorsList} store="${store}" />
            </main>
          `}
      ${store.modal && html`<${Modal} store="${store}" />`}
    `;
  }
}

export { render, html, App };
