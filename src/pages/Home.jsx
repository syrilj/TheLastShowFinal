import { useOutletContext } from "react-router-dom";
import Obituaries from "./Obituaries";

function Home() {
  const[obituaries, uuid, setObituaries] = useOutletContext();

  console.log("Home Page:"+obituaries);
  return (
    <div className="flex justify-center">
      {obituaries === undefined ? (
        <div id="BlankCard-holder">No Obituary Yet.</div>
      ) : (
        <Obituaries obituaries={obituaries} />
      )}
    </div>
  );
  
}
  
export default Home;