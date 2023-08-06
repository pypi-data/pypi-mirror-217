<div class="text-column">
 <h2 style="margin-top: 5px; text-indent: 390px; font-size: 3em">A.D.E.S.O.</h2>
 <h2 style="margin-top: 5px; text-indent: 150px">
     <b>A</b>pplication for
     <b>D</b>ecryption, <b>E</b>ncryption and
     <b>S</b>teganographic <b>O</b>perations
 </h2>
 <h2 style="margin-top: 50px;"><b>Summary:</b></h2>
 <p style="margin-top: 0px;">
  <a href="https://csrc.nist.gov/glossary/term/steganography">Steganography</a>
  is the practice of concealing information within another message to avoid detection.
  <br><br><a href="https://www.nist.gov/cryptography">Encryption</a>
  is the process of converting plaintext into ciphertext, which is unreadable.
  <br><br> This application provides both of these functionalities.  Users can first encrypt their data, via
  a password using an AES-128 algorithm in CBC mode. <br><br>Then, users can hide the encrypted data (ciphertext)
  within an image of their choice via steganography.
 </p>
 <h2 style="margin-top: 30px;"><b>Key Features:</b></h2>
 <ul style="margin-top: 5px;">
  <li>A web interface is provided to paste large plaintext objects without a terminal buffer limit.</li>
  <br>
  <li>All encryption, decryption, encoding and decoding is done in memory.</li>
 </ul>
 <h2 style="margin-top: 30px;"><b>Tools Used:</b></h2>
 <ul style="margin-top: 5px;">
  <li>Front end: <a href="https://svelte.dev/">Svelte</a> using <a href="https://kit.svelte.dev/">SvelteKit</a> </li>
  <br>
  <li>API: <a href="https://www.python.org/">Python 3.11.1 </a> using <a href="https://pypi.org/project/Flask/">Flask 2.3.2</a> </li>
  <br>
  <li>Cryptography: <a href="https://pypi.org/project/cryptography/">cryptography 41.0.1</a> </li>
  <br>
  <li>Steganography using <a href="https://wiki.bi0s.in/forensics/lsb/">LSB</a></li>
 </ul>
 <h2 style="margin-top: 30px;"><b>Gotchas:</b></h2>
 <ul style="margin-top: 5px;">
  <li>Large ciphertext and images can result in API lag or lockups for steganography.</li>
  <br>
  <li>The decode operation is done on the file selected, not the image displayed on the UI.</li>
 </ul>
 <h2 style="margin-top: 50px;"><b>Links:</b></h2>
 <p style="margin-top: 0px;">
 <li><a href="https://wiki.bi0s.in/forensics/lsb/">Read the Docs</a></li>
 <br>
 <li><a href="https://wiki.bi0s.in/forensics/lsb/">PyPi Production</a></li>
 <br>
 <li><a href="https://wiki.bi0s.in/forensics/lsb/">PyPi Test</a></li>
 <h2 style="margin-top: 30px;"><b>Installation:</b></h2>
 <code>pip install adeso</code>
</div>
