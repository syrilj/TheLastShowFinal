import { useOutletContext } from "react-router-dom";

function Home() {
  const [[obituaries]] = useOutletContext();
  return <div id="BlankCard-holder">No Obituary Yet.</div>;
}
  
export default Home;