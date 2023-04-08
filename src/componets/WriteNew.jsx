import { useState } from "react";

function WriteNew(){
    const [name, setName] = useState("");
    const [when, setWhen] = useState(""); //for birthselect
    const [death, setDeath] = useState(""); //for deathselect
    const [file, setFile] = useState(null);

    const onSubmitForm = (e) => {
        e.preventDefault();
        console.log(name, when, file);
        const data = new FormData();
        data.append("file", file);
        data.append("name", name);
        data.append("when", when);

        // Send form data to server using fetch or axios or any other library
        // ...
        
        // Redirect user to desired page implment later once other componets come later 
        window.location.href = "/";
    };

    const onFileChange = (e) => {
        console.log(e.target.files);
        setFile(e.target.files[0]);
    };

    return (
        <div className="WriteNew">
            <h2 class="WriteNewobituarytext"> Create a New Obituary</h2>
            <form class="formdiv" onSubmit={onSubmitForm}>
                <div class="imgselectdiv">
                    <input
                        className="imgselect"
                        type="file"
                        required
                        accept="images/*"
                        onChange={onFileChange}
                    />
                </div>
               
                <div class="nameboxdiv"> 
                    <input 
                        className="namebox"
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Name of the deceased"
                        required
                    /> 
                </div>

                <i>Born:  </i> 
                <input
                    className="birthselect"
                    value={when}
                    onChange={(e) => setWhen(e.target.value)}
                    type="datetime-local"
                    required
                />

                &emsp; &emsp; &emsp; &emsp; &emsp; 
                <i>Died:  </i> 
                <input
                    className="deathselect"
                    value={death}
                    onChange={(e) => setDeath(e.target.value)}
                    type="datetime-local"
                    required
                />

                <button class="writeobituarybutton"> Write Obituary</button>
            </form>
        </div>
    );
}

export default WriteNew;
