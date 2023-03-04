import { trackList } from "../globalStores";


const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
// let pianoroll
let maxMidiNumber
let minMidiNumber
export const createVerticalKeyboard = (id, width = null) => {
  const currentTrackList = trackList()
  const height = currentTrackList.selectTrack(id).pianoroll.pianorollHeight
  const pianoroll = document.getElementById(`pianoroll-${id}`)
  const svgElements = pianoroll.querySelector(`div:nth-of-type(3) svg`);
  
  const notes = Array.from(svgElements.querySelectorAll('.note'));
  const pitches = notes.map(note => Number(note.getAttributeNS(null, 'data-pitch'))); // získání všech hodnot 'data-pitch' jako pole čísel
  maxMidiNumber = Math.max(...pitches)
  minMidiNumber = Math.min(...pitches)
  // const instruments = notes.map(note => Number(note.getAttributeNS(null, 'data-instrument')))
  // const uniqueInstruments = Array.from(new Set(instruments));

  // const colors = [];
  // for (let i = 0; i < uniqueInstrumentsNum.length; i++) {
  //   const color = `rgb(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 1)`;
  //   colors.push(color);
  // }
  // uniqueInstrumentsNum.forEach((instNum, index) => {setInstrumentColor(notes, instruments, instNum, colors[index]);});

    const pitchAccidentals = {};
    for (let i = minMidiNumber; i <= maxMidiNumber; i++) {
        const hasAccidentalNote = hasAccidental(i); 
        pitchAccidentals[i] = hasAccidentalNote;
    }


  const numOfKeys = Object.keys(pitchAccidentals).length;
  const keyHeight = Math.round(height / numOfKeys)

  //Set height of pianoroll element
  pianoroll.config = {noteHeight: keyHeight}
  if(width){
    pianoroll.config = {pixelsPerTimeStep: width, noteHeight: keyHeight}
  }
 
  const keyboard = document.createElement("div");
  keyboard.style.display = "flex";
  keyboard.style.flexDirection = "column";
  keyboard.style.height = (numOfKeys * keyHeight) + "px";
  keyboard.style.width = 40 + "px";
  keyboard.style.marginTop = keyHeight * 2 + "px"; //there is margin because of visualization


  const keyboardDiv = document.getElementById(`keyboard-${id}`)
  if (keyboardDiv.hasChildNodes()) {
    keyboardDiv.removeChild(keyboardDiv.firstChild);
  }
  
  let currentMaxMidiNumber = maxMidiNumber
  while (currentMaxMidiNumber >= minMidiNumber) {
  const key = document.createElement("div");
  key.style.flexGrow = 1;
  key.style.height = keyHeight + "px";
  key.style.borderBottom = "1px solid gray ";
  key.style.borderRight = "1px solid gray ";

  keyboard.appendChild(key);

  if(!pitchAccidentals[currentMaxMidiNumber]){
      

      key.style.backgroundColor = 'white'
      // key.style.borderTop = "1px solid gray ";
  } else {
      key.style.backgroundColor = 'black'
      key.style.width = '100%'

      const blackKey = document.createElement("div");
      blackKey.style.height = keyHeight + "px";
  
      blackKey.style.backgroundColor = 'white'
      blackKey.style.width = '20%'
      blackKey.style.float = 'right'
      // blackKey.style.border = 'white'
      // key.appendChild(blackKey);
  } 
  
  if(['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7'].includes(getNoteName(currentMaxMidiNumber)) || (currentMaxMidiNumber == maxMidiNumber) || (currentMaxMidiNumber == minMidiNumber)){
    createKeyDescription(key,keyHeight,currentMaxMidiNumber  )
  }

  currentMaxMidiNumber--
}

document.getElementById(`keyboard-${id}`).appendChild(keyboard);
currentTrackList.selectTrack(id).pianoroll.isPianorollLoading = false

}
// const setSize = (size) => {

//   pianoroll.config = {noteHeight: size/(maxMidiNumber-minMidiNumber)}

// }


function hasAccidental(midiNumber) {
  const noteName = noteNames[midiNumber % 12];
  return noteName.includes('#') || noteName.includes('b');
}

function getNoteName(midiNumber) {
  const octave = Math.floor(midiNumber / 12) - 1;
  const noteName = noteNames[midiNumber % 12];
  return noteName + octave;
 }

const createKeyDescription = (key, keyHeight, currentMaxMidiNumber) => {
  const text = document.createElement("div");
  text.style.height = keyHeight + "px";
  text.textContent = getNoteName(currentMaxMidiNumber)

  text.id = 'noteName'
  text.style.marginLeft = '41px'
  text.style.marginTop = '-10px'
  text.style.position = 'absolute'
  text.style.fontSize = '12px'
  text.style.fontWeight = 'bold'
  text.style.color = 'red'
  


  key.appendChild(text)
}


const setInstrumentColor = (notes, instruments, numberOfInstrument, color) => {
  notes.forEach((element, id) => {
      if(instruments[id] == numberOfInstrument){
          element.setAttributeNS(null, 'fill', color)
      }
  });
}
