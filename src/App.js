import React from 'react';
import BlankCard from './BlankCard'
import WriteNew from './WriteNew'
import Design from './Design'
import Obituaries from './componets/Obituaries';
function App() {
  const[showDesign, setShowDesign] = useState(false);
  const[showWriteNew, setShowWriteNew] = useState(false);

  const handleWriteClick = () =>{
    setShowWriteNew(true);
  }

  const onWrite = async (obituaryData) => {
    setObituaries([obituaryData, ...obituaries]);// using a LRU replacement policy 
    setShowWriteNew(false);
  }
  return (
  <div id="container">
        <header>
          <div id="app-header">
            <h1 id="app-moto">The Last Show</h1>
          </div>
          <aside>
            <button onClick={handleWriteClick} id="menu-button">
              + New Obituary
            </button>
          </aside>
        </header>
        {!showCreate && obituaries.length === 0 ? <Empty /> : null}
        {!showCreate && obituaries.length > 0 ? (
          <Obituaries obituaries={obituaries} />
        ) : null}
        {showWriteNew ? <Create onCreate={onWrite} /> : null}
      </div>
    );
  }

export default App;
