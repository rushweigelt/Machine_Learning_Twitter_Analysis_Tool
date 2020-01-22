var GaussianNB = function(priors, sigmas, thetas) {

    this.priors = priors;
    this.sigmas = sigmas;
    this.thetas = thetas;

    this.predict = function(features) {
        var likelihoods = new Array(this.sigmas.length);
    
        for (var i = 0, il = this.sigmas.length; i < il; i++) {
            var sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.log(2. * Math.PI * this.sigmas[i][j]);
            }
            var nij = -0.5 * sum;
            sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.pow(features[j] - this.thetas[i][j], 2.) / this.sigmas[i][j];
            }
            nij -= 0.5 * sum;
            likelihoods[i] = Math.log(this.priors[i]) + nij;
        }
    
        var classIdx = 0;
        for (var i = 0, l = likelihoods.length; i < l; i++) {
            classIdx = likelihoods[i] > likelihoods[classIdx] ? i : classIdx;
        }
        return classIdx;
    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 8) {

        // Features:
        var features = process.argv.slice(2);

        // Parameters:
        var priors = [0.4627645874309263, 0.5372354125690737];
        var sigmas = [[1.7191224487439596, 0.49931392346466835, 1.0000000000061479e-09, 0.39423819406656924, 2.1589831901724783, 0.08013330927070371, 1.7242625703933008, 0.7208362790016991], [0.29805355730393335, 1.3741302632440102, 1.8536601778649304, 1.5217699053219904, 1.1396959434244894e-06, 1.5674430704913462, 0.37538899013970056, 1.161620895196453]];
        var thetas = [[-0.22684642632952035, -0.18879828317181963, -0.06939487457885124, -0.0037079188672970703, 0.03229555840879158, -0.37453450532254695, 0.02155154404191916, -0.2217548578706768], [0.19540129044824797, 0.1626273279381607, 0.059775453651404874, 0.003193932314776081, -0.027818793052600762, 0.32261705349392705, -0.018564099003407095, 0.19101550812137602]];

        // Estimator:
        var clf = new GaussianNB(priors, sigmas, thetas);
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}