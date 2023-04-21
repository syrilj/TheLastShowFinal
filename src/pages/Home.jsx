import { useOutletContext } from "react-router-dom";
import Obituaries from "../components/Obituaries";

function Home() {
  const[obituaries, uuid, setObituaries] = useOutletContext();

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