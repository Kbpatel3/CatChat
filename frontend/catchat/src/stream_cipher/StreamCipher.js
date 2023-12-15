class StreamCipher {
    constructor(keyString) {
        const encoder = new TextEncoder();
        this.key = encoder.encode(keyString); // Convert string key to byte array
    }

    generateKeystream(length) {
        let keystream = new Uint8Array(length);
        for (let i = 0; i < length; i++) {
            keystream[i] = this.key[i % this.key.length];
        }
        return keystream;
    }

    encrypt(plaintext) {
        const encoder = new TextEncoder();
        const plaintextBytes = encoder.encode(plaintext);
        const keystream = this.generateKeystream(plaintextBytes.length);
        const ciphertext = new Uint8Array(plaintextBytes.length);
        for (let i = 0; i < plaintextBytes.length; i++) {
            ciphertext[i] = plaintextBytes[i] ^ keystream[i];
        }
        return ciphertext;
    }

    decrypt(ciphertext) {
        const keystream = this.generateKeystream(ciphertext.length);
        const plaintextBytes = new Uint8Array(ciphertext.length);
        for (let i = 0; i < ciphertext.length; i++) {
            plaintextBytes[i] = ciphertext[i] ^ keystream[i];
        }
        const decoder = new TextDecoder();
        return decoder.decode(plaintextBytes);
    }
}

export default StreamCipher;
