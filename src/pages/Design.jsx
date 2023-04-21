import { Link, Outlet } from "react-router-dom"
import { useEffect, useState } from "react";
import axios from "axios";
import { v4 as uuidv4 } from 'uuid';

import Header from "../components/Header";

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
    }).catch((error) => {
      console.error(error);
    });
  }, [uuid]);

  return (
    <div className="flex flex-col h-screen">
      <Header obituaries={obituaries} uuid={uuid} setObituaries={setObituaries} />
      <div className="flex-1">
        <Outlet context={[obituaries, uuid, setObituaries]} />
      </div>
    </div>


  );
}

export default Design;

