import { Link, Outlet } from "react-router-dom"


function Design() {
  return (
    <div id="container">
      <header>
        <div id="app-header">
          <h1 id="app-moto">The Last Show</h1>
        </div>
        <aside>
        <Link to="/newObituary"><button id="menu-button">+ New Obituary</button> </Link>
        </aside>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}

export default Design;

