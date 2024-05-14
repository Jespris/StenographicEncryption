Stenography program

Stenography, or hiding data in pictures, is a tool used mainly by malware to obfuscate data. Many different techniques exist already, this is one example of them that I implemented myself. TO BE CLEAR THIS IS NOT MALWARE!!!

The program consists of two parts: Encryption and Decryption

Encryption:
  To encrypt some data, we need three things:
  - An input image, preferably large to be able to encrypt a lot of data without detection
  - Data to encrypt, in my program this is simply a string to be printed. This could be the malware payload.
  - An encryption key, used to obfuscate the data in a specific way
    
  This programs encryption method goes something like this:
  1. The key determines which byte index in the image pixel datablock the encrypted data should start at
  2. The key determines how the pixel colour changes, possibly by adding a segment of the input as hex value to the pixel hex value, modified by the key
  3. We now have an encrypted image that looks slightly different to the one we started with

Decryption:
  To decrypt the data we need two things:
  - The image to decrypt
  - The decryption key, which is a copy of the encryption key.
  With these things we can deobfuscate the data by doing the encryption process in reverse


Jesper Andersson
Project started in May 2024
