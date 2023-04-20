import { Link, Outlet } from "react-router-dom"
import { useEffect, useState } from "react";
import axios from "axios";
import { v4 as uuidv4 } from 'uuid';

function Design() {

  const [obituaries, setObituaries] = useState([]);
  const [uuid, setUuid] = useState("");

  
  //On load, get uuid from local storage if it exists, otherwise create a new one
  useEffect(() => {
    const uuid = localStorage.getItem("uuid");
    if (uuid) {
      setUuid(uuid);
      console.log("Existing uuid found: ", uuid);
    } else {
      const newUuid = uuidv4();
      localStorage.setItem("uuid", newUuid);
      setUuid(newUuid);
      console.log("New uuid created: ", newUuid);
    }
  }, []);

  useEffect(() => {
    if(!uuid) return;
    const baseURL = `https://ndc7f3imz4ovejqaz2wek3qwfy0jwmxk.lambda-url.ca-central-1.on.aws/`;
    const config = { 
      headers: {
        'uuid': uuid
      }
    };
    axios.get(`${baseURL}`, config).then((response) => {
      setObituaries(response.data);
      console.log(response.data);
    }).catch((error) => {
      console.error(error);
    });
  }, [uuid]);



  



  return (
    <div id="container">
      <header>
        <div id="app-header">
          <Link to="/"><h1 id="app-moto">The Last Show</h1></Link>
        </div>
        <aside>
        <Link to="/newObituary"><button id="menu-button">+ New Obituary</button> </Link>
        </aside>
      </header>
      <main>
        <Outlet context={[obituaries, uuid, setObituaries]} />
      </main>
    </div>
  );
}

export default Design;

